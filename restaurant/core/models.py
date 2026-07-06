from django.db import models


class MenuCategory(models.Model):
    name = models.CharField(max_length=80,unique=True)
    slug = models.SlugField(max_length=90,unique=True)
    
    class Meta:
        verbose_name = "Menu Category"
        verbose_name_plural = "Menu Categories"
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    

class MenuTag(models.Model):
    name = models.CharField(max_length=50,unique=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory,on_delete=models.SET_NULL,null=True,related_name='items')
    title = models.CharField(max_length=80)
    description = models.TextField()
    image = models.ImageField(upload_to='menu/',blank=True, null=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    rating = models.DecimalField(max_digits=3,decimal_places=2,default=5.0)
    review_count = models.PositiveIntegerField(default=0)
    calories = models.PositiveIntegerField(blank=True,null=True)
    prep_time = models.PositiveIntegerField(blank=True,null=True,help_text="Preparation time in minutes")
    tags = models.ManyToManyField(MenuTag,blank=True,related_name="menu_items")
    is_featured = models.BooleanField(default=False)
    is_hot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
    

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Gallery"
        verbose_name_plural = "Gallery"

    def __str__(self):
        return self.title