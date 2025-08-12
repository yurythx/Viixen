from django.contrib import messages


class SuccessMessageMixin:
    """
    A mixin that adds a success message when a form is valid.
    
    Usage:
        class MyView(SuccessMessageMixin, CreateView):
            success_message = "Object created successfully!"
    """
    success_message = None
    
    def form_valid(self, form):
        """
        Add a success message if one is configured.
        """
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response
    
    def delete(self, request, *args, **kwargs):
        """
        Add a success message on successful delete if one is configured.
        """
        response = super().delete(request, *args, **kwargs)
        if hasattr(self, 'delete_success_message') and self.delete_success_message:
            messages.success(self.request, self.delete_success_message)
        return response
