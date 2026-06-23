# Django is a high-level Python web framework used to build:websites,web applications,APIs,admin panels,authentication systems,quickly and securely.Instead of creating everything from scratch.

from django.db import models

# This line imports Django’s database model system.

from django.contrib.auth.models import User

# This line imports Django’s built-in User model, which is used for authentication and user management

# Create your models here.


class UserProfile(models.Model):
    # creating a new database table called UserProfile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # This creates a one-to-one relationship with Django's built-in User model.
    # If the user is deleted: the corresponding UserProfile will also be deleted (cascade delete).
    Phone = models.CharField(max_length=15, blank=True)
    # This adds a new field to the UserProfile model to store the user's phone number.

    def __str__(self):
        return self.user.username


# This method defines how the UserProfile object will be represented as a string, which is useful for debugging and display purposes. It returns the username of the associated User object.


class Prediction(models.Model):
    # creating a new database table called Predictions.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="predictions")
    # This creates a foreign key relationship with Django's built-in User model, allowing multiple predictions to be associated with a single user. If the user is deleted, all related predictions will also be deleted (cascade delete).
    N = models.FloatField()  # This adds a new field
    P = models.FloatField()
    K = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    predicted_label = models.CharField(max_length=100)
    # This adds a new field to store the predicted label(rice,maize,wheat,kidney beans) for the crop recommendation.
    created_at = models.DateTimeField(auto_now_add=True)
    # This adds a timestamp field that automatically records the date and time when a prediction is created.

    class Meta:
        ordering = ["-created_at"]

    # This specifies that when querying the Predictions model, the results should be ordered by the created_at field in descending order (newest first).(Last ma create(matlab bharkhar gareyko) gareyko prediction pahila dekhaune)

    def __str__(self):
        return f"{ self.user.username}'s Prediction"
