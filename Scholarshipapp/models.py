import calendar
from datetime import datetime
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.

class Scholarship_category(models.Model):
    objects = None
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=350)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='Scholarship_category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'scholarship_category'
        verbose_name_plural = 'scholarship_categories'

    def get_url(self):
        return reverse('Scholarshipapp:addcat', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Scholarship_item(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=350, null=False)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_date = models.DateTimeField(auto_now_add=True, editable=False)
    offered_by = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=250)
    category = models.ForeignKey(Scholarship_category, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'scholarship_item'
        verbose_name_plural = 'scholarship_items'

    def get_url(self):
        return reverse('Scholarshipapp:addscholarship', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class S_Category(models.Model):
    S_Category=models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id} : {self.S_Category}'
    
class All_Scholarship(models.Model):
    All_Scholarship=models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id} : {self.All_Scholarship}' 

class States(models.Model):
    States=models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id} : {self.States}'    

class Education(models.Model):
    Education=models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id} : {self.Education}'       

class Eligibility(models.Model):
    Eligibility1=models.CharField(max_length=30)
    Eligibility2=models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id} : {self.Eligibility1}'     
    
class Plan(models.Model):
    Plan=models.CharField(max_length=30)
    Plan_Amount=models.IntegerField()
    PLan_Duration=models.CharField(max_length=30)
    Plan_Description=models.TextField(max_length=30)

    def __str__(self):
        return f'{self.id} : {self.Plan}'     
    
class Register(models.Model):
    u_name=models.CharField(max_length=30,null=True,blank=True)
    f_Name=models.CharField(max_length=30)
    l_Name=models.CharField(max_length=30)
    dob=models.CharField(max_length=30,null=True,blank=True)
    Mob=models.CharField(max_length=10)
    Email=models.EmailField()
    S_Category=models.ForeignKey(S_Category,on_delete=models.DO_NOTHING,null=True,blank=True)
    Education=models.ForeignKey(Education,on_delete=models.DO_NOTHING,null=True,blank=True)
    Password=models.CharField(max_length=30)
    # Re_Password=models.CharField(max_length=30,null=True,blank=True)
    States=models.ForeignKey(States,on_delete=models.DO_NOTHING,null=True,blank=True)
    
    def __str__(self):
        return f'{self.id} : {self.f_Name}' 
    
class Scholarship_details(models.Model):
    Scholarship_logo=models.FileField(upload_to='scholarship_logo',null=True)
    Scholarship_name=models.CharField(max_length=30)
    Offered_by=models.CharField(max_length=30)
    # Plan_status=models.CharField(max_length=30)
    Award=models.IntegerField()
    S_Category=models.ManyToManyField(S_Category,blank=True)
    Eligibility=models.ManyToManyField(Eligibility,blank=True)
    Education=models.ManyToManyField(Education,blank=True)
    All_Scholarship=models.ManyToManyField(All_Scholarship,blank=True)
    States=models.ManyToManyField(States,blank=True)
    # Time_field=models.TimeField(auto_now_add=True)
    Published_date=models.DateTimeField(null=True, blank=True)
    Dead_line=models.DateTimeField(null=True, blank=True)
    Scholar_Description=models.TextField(max_length=500,null=True,blank=True)

    def __str__(self):
        return f'{self.id} : {self.Scholarship_name}'     

class User_Plan(models.Model):
    plan_name=models.CharField(max_length=30)
    plan_price=models.IntegerField()    
    plan_image=models.FileField(upload_to='plan_image',null=True)

    def __str__(self):
        return f'{self.id} : {self.plan_name}' 

class User_Profile(models.Model):
    user=models.ForeignKey(Register,on_delete=models.DO_NOTHING,null=True,blank=True)
    address = models.CharField(max_length=255)
    u_father=models.CharField(max_length=30)
    u_f_mob=models.CharField(max_length=10)
    u_mother=models.CharField(max_length=30)
    u_m_mob=models.CharField(max_length=10)
    u_image=models.FileField(upload_to='user_image',null=True)
    u_certificate=models.FileField(upload_to='user_certificate',null=True)
    
    def __str__(self):
        return f'{self.id} : {self.user}'  
    
class UserPlanScholarship(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    u_plan = models.ForeignKey(User_Plan, on_delete=models.CASCADE)
    chosen_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.u_plan.plan_name

class upcoming_scholarship(models.Model):
    up_schol_name=models.CharField(max_length=30)
    up_schol_publish_date=models.DateField(null=True,blank=True)
    up_schol_publish_desc= models.CharField(max_length=255)    

class applied_scholarship(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship_details, on_delete=models.CASCADE)
    applied_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.f_Name} - {self.scholarship.Scholarship_name}"
    
class exam_calender(models.Model):
    xam_date=models.DateField(null=True,blank=True) 
    xam_name=models.CharField(max_length=50)   

    def __str__(self):
        return f"{self.xam_date}"
    
class my_wishlist(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    scholarships = models.ManyToManyField(Scholarship_details)
    applied_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.f_Name}"    
    
class Approval(models.Model):
    status_choices = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=30, choices=status_choices, default='Pending')
    user = models.ForeignKey(Register, on_delete=models.CASCADE,null=True,blank=True)
    applied_scholarship = models.ForeignKey(applied_scholarship, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.id} : {self.status}'     


class AdminUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)      
