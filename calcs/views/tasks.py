from celery import shared_task


@shared_task
def args_to_function(arguments, arg_names):
    # TODO: replace with actual task
    return arguments