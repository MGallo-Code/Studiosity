from django.db import models

# class UserModel(models.Model):
#     """
#     """
#     username = models.CharField(max_length=25, unique=True, null=False)
#     profile_image = models.OneToOneField(
#         ImageFile, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True, 
#         related_name='profile_image_user'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"User {self.id}: {self.username}"