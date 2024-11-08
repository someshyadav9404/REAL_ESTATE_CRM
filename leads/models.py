from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save, pre_delete 
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from decimal import Decimal
from django.shortcuts import get_object_or_404

import logging
logger = logging.getLogger('app_errors')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

# Signal to log changes to the User model
@receiver(post_save, sender=User)
def log_user_activity(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New user created: {instance.username}, is_organisor={instance.is_organisor}, is_agent={instance.is_agent}")
    else:
        logger.info(f"User updated: {instance.username}, is_organisor={instance.is_organisor}, is_agent={instance.is_agent}")



# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.IntegerField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Signal to log changes to the UserProfile model
@receiver(post_save, sender=UserProfile)
def log_user_profile_activity(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New UserProfile created: {instance.user.username}, Full Name: {instance.full_name}, Contact: {instance.contact_number}, Email: {instance.email}")
    else:
        logger.info(f"UserProfile updated: {instance.user.username}, Full Name: {instance.full_name}, Contact: {instance.contact_number}, Email: {instance.email}")
   
#New Addition
class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
# New Addition Ended

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category",related_name="leads" ,null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()   
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")
    converted_date = models.DateTimeField(null=True, blank=True) 
    objects = LeadManager()

# New Added profile picture, converted date and objects
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def save(self, *args, **kwargs):
        # Check if it's a new instance or an update
        is_new_instance = self.pk is None

        # Call the parent save method to save the instance to the database
        super().save(*args, **kwargs)

        # Directly log to check if logging works
        logger.info("Testing if logging works.")

        # Log the action (whether it is a creation or an update)
        if is_new_instance:
            action = "created"
        else:
            action = "updated"

        # Log the instance data (exclude internal attributes)
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Lead instance {self.pk} was {action}. Data: {data}')

    def delete(self, *args, **kwargs):
        # Log the deletion action with instance data before deleting
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Lead instance {self.pk} is about to be deleted. Data: {data}')
        
        # Call the parent delete method to actually delete the instance
        super().delete(*args, **kwargs)

        # Log after deletion
        logger.info(f'Lead instance {self.pk} was deleted. Data: {data}')



# File upload logging for follow-ups

def handle_upload_follow_ups(instance, filename):
    logger.info(f"Follow-up file uploaded for Lead ID: {instance.lead.pk}, File: {filename}")
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"

# FollowUp Model with Logging
class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, related_name="followups", on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to=handle_upload_follow_ups)

    # Add the status field
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('postponed', 'Postponed'),
        ('in-Progress', 'In-Progress'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.last_name}"

    def save(self, *args, **kwargs):
            # Check if it's a new instance or an update
            is_new_instance = self.pk is None

            # Call the parent save method to save the instance to the database
            super().save(*args, **kwargs)

            # Log the action (whether it's creation or update)
            action = "created" if is_new_instance else "updated"
            
            # Log the instance data, excluding internal attributes
            data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
            logger.info(f'FollowUp instance {self.pk} was {action}. Data: {data}')

    def delete(self, *args, **kwargs):
        # Log the deletion action with instance data before deleting
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'FollowUp instance {self.pk} is about to be deleted. Data: {data}')
            
        # Call the parent delete method to actually delete the instance
        super().delete(*args, **kwargs)

            # Log after deletion
        logger.info(f'FollowUp instance {self.pk} was deleted. Data: {data}')

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    parent_agent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_agents')
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Percentage of profit shared
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Total profit earned
    level = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        # Check if this is a new instance or an update
        is_new_instance = self.pk is None

        # Call the parent save method to save the instance to the database
        super().save(*args, **kwargs)

        # Log creation or update action
        action = "created" if is_new_instance else "updated"
        
        # Log the instance data, excluding internal attributes
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Agent instance {self.pk} was {action}. Data: {data}')

    def delete(self, *args, **kwargs):
        # Log the deletion action before deletion
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Agent instance {self.pk} is about to be deleted. Data: {data}')

        # Manually delete the associated UserProfile and User before deleting the Agent
        if self.organisation:
            self.organisation.delete()  # Delete associated UserProfile
            logger.info(f'Associated UserProfile for Agent {self.pk} was deleted.')
        if self.user:
            self.user.delete()  # Delete associated User
            logger.info(f'Associated User for Agent {self.pk} was deleted.')

        # Call the parent delete method to actually delete the Agent instance
        super().delete(*args, **kwargs)

        # Log after deletion
        logger.info(f'Agent instance {self.pk} was deleted.')

class Category(models.Model):
    name = models.CharField(max_length=30)  # New, Contacted, Converted, Unconverted
    organisation = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)

    def __str__(self):
        # Log whenever a Category instance is accessed
        logger.info(f"Category accessed: {self.name} (ID: {self.pk})")
        return self.name

    def save(self, *args, **kwargs):
        # Check if the instance is new (creation) or existing (update)
        is_new_instance = self.pk is None

        # Save the instance
        super().save(*args, **kwargs)

        # Log creation or update action
        action = "created" if is_new_instance else "updated"
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Category instance {self.pk} was {action}. Data: {data}')

    def delete(self, *args, **kwargs):
        # Log the deletion action before the instance is deleted
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Category instance {self.pk} is about to be deleted. Data: {data}')

        # Delete the instance
        super().delete(*args, **kwargs)

        # Log after deletion
        logger.info(f'Category instance {self.pk} was deleted.')

# Signal handler for UserProfile creation
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        logger.info(f"UserProfile created for user: {instance.username}")
        UserProfile.objects.create(user=instance)
        
post_save.connect(post_user_created_signal, sender=User)

class Salary(models.Model):
    agent = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # Or your Agent model
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New commission field
    payment_date = models.DateField()
    organisation = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.DO_NOTHING)
    property = models.ForeignKey('Property', null=True, blank=True, on_delete=models.DO_NOTHING)  # Link to Property model

    def total_compensation(self):
        """Calculate the total compensation including salary, bonus, and commission."""
        total = self.base_salary + (self.bonus or 0) + self.commission
        return total

    def __str__(self):
        # Log when the Salary instance is accessed
        logger.info(f"Salary accessed: Agent={self.agent.username}, Payment Date={self.payment_date}")
        return f"Salary for {self.agent.username} on {self.payment_date}"

    def save(self, *args, **kwargs):
        # Determine if the instance is new or being updated
        is_new_instance = self.pk is None

        # Save the instance
        super().save(*args, **kwargs)

        # Log creation or update
        action = "created" if is_new_instance else "updated"
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Salary instance {self.pk} was {action}. Data: {data}')

    def delete(self, *args, **kwargs):
        # Log before deletion
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Salary instance {self.pk} is about to be deleted. Data: {data}')

        # Delete the instance
        super().delete(*args, **kwargs)

        # Log after deletion
        logger.info(f'Salary instance {self.pk} was deleted.')

class Sale(models.Model):
    property = models.ForeignKey('Property', on_delete=models.DO_NOTHING)
    agent = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    sale_price = models.DecimalField(max_digits=15, decimal_places=2)
    sale_date = models.DateField()
    organisation = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        # Determine if the instance is new or being updated
        is_new_instance = self.pk is None

        # Save the instance
        super().save(*args, **kwargs)

        # Mark the property as sold after the sale is saved
        if self.property:
            self.property.is_sold = True
            self.property.save()

        # Log creation or update
        action = "created" if is_new_instance else "updated"
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Sale instance {self.pk} was {action}. Data: {data}')

    def delete(self, *args, **kwargs):
        # Log before deletion
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Sale instance {self.pk} is about to be deleted. Data: {data}')

        # Delete the instance
        super().delete(*args, **kwargs)

        # Log after deletion
        logger.info(f'Sale instance {self.pk} was deleted.')

    def __str__(self):
        # Log when the Sale instance is accessed
        logger.info(f"Sale accessed: Agent={self.agent.username}, Sale Price=${self.sale_price}")
        return f"Sale by {self.agent.username} for ${self.sale_price}"

## Project
class Project(models.Model):
    project_name = models.CharField(max_length=255)
    block = models.CharField(max_length=2)
    kisans = models.ManyToManyField('Kisan', related_name='projects_kisan')
    dev_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    title = models.CharField(unique=True, max_length=255)
    lands = models.ManyToManyField('Kisan', related_name='projects_lands')
    type = models.CharField(max_length=255, null=True, blank=True)
    total_land_available_fr_plotting = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_development_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def create_composite_key(self):
        letters = f"{self.project_name[:]}".upper()
        bl = f"{self.block[:]}".upper()
        composite_key = f"{letters}-{bl}"
        logger.info(f"Composite key generated: {composite_key}")
        return composite_key

    def save(self, *args, **kwargs):
        # Check if it's a new instance
        is_new_instance = self.pk is None

        # Generate and set the title before saving
        self.title = self.create_composite_key()
        
        # Save the instance
        super().save(*args, **kwargs)

        # Update the title field directly in the database after saving
        self.__class__.objects.filter(pk=self.pk).update(title=self.title)

        # Log creation or update
        action = "created" if is_new_instance else "updated"
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Project instance {self.pk} was {action}. Data: {data}')

    def delete(self, *args, **kwargs):
        # Log before deletion
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Project instance {self.pk} is about to be deleted. Data: {data}')

        # Perform the deletion
        super().delete(*args, **kwargs)

        # Log after deletion
        logger.info(f'Project instance {self.pk} was deleted.')

    def __str__(self):
        # Log access to the Project instance
        logger.info(f"Project accessed: Title={self.title}")
        return self.title

#TypeofPlot
class Typeplot(models.Model):
    type = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.type    

class Property(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    totalprice = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    breadth = models.IntegerField(null=True, blank=True)
    block = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    agent = models.ForeignKey('Agent', null=True, blank=True, on_delete=models.SET_NULL)
    project_id = models.ForeignKey('Project', null=True, blank=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey('UserProfile', null=True, blank=True, on_delete=models.DO_NOTHING)
    land = models.ForeignKey('Kisan', null=True, blank=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=7, blank=True)
    is_sold = models.BooleanField(default=False)
    is_in_emi = models.BooleanField(default=False)
    
    # Removed the redundant ForeignKey to Property itself
    related_property = models.ForeignKey('Property', null=True, blank=True, on_delete=models.DO_NOTHING) 
    PLOT_CHOICES = [
        ('Normal', 'Normal'),
        ('Corner', 'Corner'),
        ('Special', 'Special'),
    ]
    plot_type = models.CharField(max_length=50, choices=PLOT_CHOICES,default='Normal')

    def if_sold(self):
        logger.info(f"Checking if property {self.title} is sold")
        print(f"Checking if property {self.title} is sold")
        return self.is_sold  # Ensure this references the correct model
    
    def __str__(self):
        return self.title
    
    def create_composite_key(self):
        letters = "PRP"  # Ensure uppercase
        formatted_number = f"{self.id:03}"  # Pads with zeros if necessary
        composite_key = f"{letters}-{formatted_number}"
        logger.info(f"Composite key generated for property: {composite_key}")
        return composite_key

    def save(self, *args, **kwargs):
        is_new_instance = self.pk is None

        if not self.title:
            self.title = self.create_composite_key()

        super().save(*args, **kwargs)
        self.__class__.objects.filter(pk=self.pk).update(title=self.title)

        action = "created" if is_new_instance else "updated"
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Property instance {self.pk} was {action}. Data: {data}')

    def delete(self, *args, **kwargs):
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        logger.info(f'Property instance {self.pk} is about to be deleted. Data: {data}')

        super().delete(*args, **kwargs)

        logger.info(f'Property instance {self.pk} was deleted.')

class Bonus(models.Model):
    agent = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_awarded = models.DateField()

    def __str__(self):
        logger.info(f"Bonus awarded to {self.agent.username}: {self.bonus_amount}")
        return f"{self.agent.username} - Bonus of {self.bonus_amount}"
    
    def save(self, *args, **kwargs):
        # Log when a bonus is saved (either newly created or updated)
        action = "created" if self.pk is None else "updated"
        super().save(*args, **kwargs)
        logger.info(f"Bonus for agent {self.agent.username} was {action} with amount {self.bonus_amount} on {self.date_awarded}")

# Area
class Area(models.Model):
    length = models.IntegerField(editable=True)
    breadth = models.IntegerField(editable=True)
    area = models.IntegerField(null=True,blank=True )

    class Meta:
        # Ensure that the combination of length and breadth is unique
        constraints = [
            models.UniqueConstraint(fields=['length', 'breadth'], name='unique_length_breadth')
        ]

    def save(self, *args, **kwargs):
        # Calculate the area before saving and log the calculation
        logger.debug(f"Calculating area for length {self.length} and breadth {self.breadth}")
        self.area = self.length * self.breadth
        super().save(*args, **kwargs)
        logger.info(f"Area instance created with length {self.length}, breadth {self.breadth}, and calculated area {self.area}")

    def __str__(self):
        # Log whenever __str__ is called
        logger.info(f"Area object created for dimensions: Length {self.length}, Breadth {self.breadth}, Area {self.area}")
        return f"Property with length {self.length} and breadth {self.breadth}"

# EMI
class EmiPlan(models.Model):
    name = models.CharField(max_length=100)  # Name of the EMI plan
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Interest rate (e.g., 8.5%)
    tenure_months = models.IntegerField()  # Number of months for EMI
    minimum_downpayment = models.DecimalField(max_digits=10, decimal_places=2)  # Minimum down payment
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        logger.info(f"EMI Plan created: {self.name}")
        return self.name
    
    def save(self, *args, **kwargs):
        # Log when an EMI plan is saved
        action = "created" if self.pk is None else "updated"
        super().save(*args, **kwargs)
        logger.info(f"EMI Plan '{self.name}' was {action} with interest rate {self.interest_rate}% and tenure {self.tenure_months} months")

# DAYBOOK
class Balance(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    carryover_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add this field

    def __str__(self):
        logger.info(f"Balance created with amount: {self.amount} and carryover amount: {self.carryover_amount}")
        return f"Balance: {self.amount}"
    
    def save(self, *args, **kwargs):
        # Log when the balance is saved (either created or updated)
        action = "created" if self.pk is None else "updated"
        super().save(*args, **kwargs)
        logger.info(f"Balance {action} with amount: {self.amount} and carryover amount: {self.carryover_amount}")

    
class Daybook(models.Model):
    ACTIVITY_CHOICES = [
        ('pantry', 'Pantry'),
        ('fuel', 'Fuel'),
        ('office_expense', 'Office Expense'),
        ('site_development', 'Site Development'),
        ('site_visit', 'Site Visit'),
        ('printing', 'Printing'),
        ('utility', 'Utility'),
        ('others', 'Others'),
    ]

    date = models.DateField(default=timezone.now)
    activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    custom_activity = models.CharField(max_length=100, blank=True, null=True)  # For "Others"
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    remark = models.TextField(blank=True, null=True)
    
    def __str__(self):
        # Log whenever __str__ is called (representing the Daybook entry)
        activity_display = self.custom_activity if self.activity == 'others' else self.activity
        logger.info(f"Daybook entry created: {self.date} - {activity_display} - Amount: {self.amount}")
        return f"{self.date} - {activity_display} - {self.amount}"

    def save(self, *args, **kwargs):
        # Handle custom activity logging if the activity is 'Others'
        if self.activity == 'others' and not self.custom_activity:
            logger.warning("Custom activity is required when activity is set to 'Others'.")
        else:
            activity_display = self.custom_activity if self.activity == 'others' else self.activity
            action = "created" if self.pk is None else "updated"
            super().save(*args, **kwargs)
            logger.info(f"Daybook entry {action} with date: {self.date}, activity: {activity_display}, amount: {self.amount}")

# PROMOTER MODEL
class Promoter(models.Model):
    # Personal Information
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()

    # Legal and Joining Information
    pan_no = models.CharField(max_length=15)
    id_card_number = models.CharField(max_length=20)
    joining_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage of joining

    def __str__(self):
        logger.info(f"Promoter created: {self.name}, Email: {self.email}")
        return self.name

# PLOT BOOKING
class PlotBooking(models.Model):
    booking_date = models.DateField()
    name = models.CharField(max_length=100)
    father_husband_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], null=True)
    custom_gender = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField()
    mobile_no = models.CharField(max_length=15)
    address = models.TextField()
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    nominee_name = models.CharField(max_length=100, blank=True, null=True)
    # PLC Charges
    corner_plot_10 = models.BooleanField(default=False)
    corner_plot_5 = models.BooleanField(default=False)
    full_pay_discount = models.BooleanField(default=False)
    location = models.CharField(max_length=255)
    project = models.OneToOneField(Property, on_delete=models.DO_NOTHING, related_name='project', unique=True,null=True, blank=True)
    associate_detail = models.BooleanField(default=False)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='plot_bookings')  # Changed to lowercase
    Plot_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    payment_type = models.CharField(max_length=50, choices=[('custom', 'Custom Payment'), ('installment', 'Installments')])
    booking_amount = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_payment = models.CharField(max_length=50, choices=[('cheque', 'Cheque'), ('rtgs', 'RTGS/NEFT'), ('cash', 'Cash')])
    payment_date = models.DateField()
    emi_tenure = models.IntegerField(blank=True, null=True)  # EMI tenure in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Interest rate as a percentage
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)  # Calculated EMI amount
    remark = models.TextField(blank=True, null=True)
    
    def update_property_status_if_paid(self):
        # Check if there are any pending EMI payments
        pending_emis = self.emi_payments.filter(status='Pending').count()
        if pending_emis == 0 and self.project:
            # All payments have been made
            property_obj = self.project
            property_obj.is_in_emi = False
            property_obj.is_sold = True
            property_obj.save()
            logger.info(f"Property status updated to sold: {property_obj.title}")
        else:
            logger.info(f"Property not yet fully paid; {pending_emis} EMI payments pending.")

    def __str__(self):
        logger.info(f"Plot Booking created: {self.name} on {self.booking_date}")
        return f"Plot Booking - {self.name} on {self.booking_date}"

    def save(self, *args, **kwargs):
        # Log when a plot booking is created or updated
        action = "created" if self.pk is None else "updated"
        super().save(*args, **kwargs)
        logger.info(f"PlotBooking {action}: {self.name} - {self.booking_date}")
    
class EMIPayment(models.Model):
    plot_booking = models.ForeignKey('PlotBooking', on_delete=models.DO_NOTHING, related_name='emi_payments')
    due_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')

    def remaining_amount(self):
        """Calculate the remaining amount to be paid."""
        remaining = self.emi_amount - self.amount_paid
        logger.debug(f"Remaining amount for EMI: {remaining} for {self.plot_booking}.")
        return remaining

    def pay_emi(self, amount):
        """Pay the EMI with the specified amount."""
        remaining = self.remaining_amount()
        
        # Log the details of the payment attempt
        logger.info(f"Attempting to pay EMI: Current Amount Paid: {self.amount_paid}, Attempting to Pay: {amount}, Remaining: {remaining}")

        if amount <= 0:
            logger.warning(f"Invalid payment attempt: Amount must be greater than zero. Payment details: {amount}")
            return {'success': False, 'message': "Payment amount must be greater than zero."}
        
        if amount > remaining:
            logger.warning(f"Payment exceeds remaining EMI: Amount exceeds {remaining}. Payment details: {amount}")
            return {'success': False, 'message': f"Payment amount cannot exceed the remaining amount of {remaining}."}

        self.amount_paid += amount

        # Update the status based on the total amount paid
        if self.amount_paid >= self.emi_amount:
            self.amount_paid = self.emi_amount
            self.status = 'Paid'
        else:
            self.status = 'Pending'

        # Save the changes to the database
        self.save()

        # Check if all EMIs for this plot booking are paid
        self.plot_booking.update_property_status_if_paid()  # Update property status based on payment status
        logger.info(f"EMI payment processed: {amount} for {self.plot_booking}. Status: {self.status}")
        return {'success': True, 'message': "Payment processed successfully."}

    def __str__(self):
        logger.info(f"EMI Payment for Plot Booking: {self.plot_booking} - Due: {self.due_date}")
        return f"EMI Payment for {self.plot_booking} - Due: {self.due_date} - Status: {self.status}"

    class Meta:
        ordering = ['due_date']  # Order EMI payments by due date


class Level(models.Model):
    level = models.CharField(max_length=222)
    interest = models.IntegerField()

    def __str__(self):
        logger.info(f"Level created: {self.level} with interest rate: {self.interest}")
        return self.level   

class Kisan(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.IntegerField()
    address = models.TextField(max_length=50)
    is_assigned = models.BooleanField(default=False)
    khasra_number = models.IntegerField(unique=True)
    area_in_beegha = models.DecimalField(max_digits=20, decimal_places=3)
    land_costing = models.DecimalField(max_digits=12, decimal_places=3)
    development_costing = models.DecimalField(max_digits=12, decimal_places=3,default=0,null=True,blank=True)
    # Make these fields optional
    kisan_payment = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,default=0)
    land_address = models.TextField(max_length=50, null=True, blank=True)
    payment_to_kisan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  
    basic_sales_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    is_sold = models.BooleanField(default=False)
    usable_land_total = models.FloatField(null=True, blank=True)
    LAND_TYPE_CHOICES = [
        ('plot', 'Plot'),
        ('rowhouse', 'Rowhouse'),
        ('flat', 'Flat'),
    ]
    
    land_type = models.CharField(max_length=50, choices=LAND_TYPE_CHOICES,default=False)

    def area_in_sqft(self):
        """Convert area from beegha to square feet."""
        convert_in_sqft = 27200
        sqft = self.area_in_beegha * convert_in_sqft
        logger.debug(f"Converted area from {self.area_in_beegha} beegha to {sqft} sqft.")
        return sqft
    
    def __str__(self) -> str:
        logger.info(f"Kisan created: {self.first_name} {self.last_name} with khasra number {self.khasra_number}")
        return f"Kisan: {self.first_name} {self.last_name}"
    
