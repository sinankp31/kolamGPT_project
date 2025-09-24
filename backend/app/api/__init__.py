from flask import Blueprint

# Create a new Blueprint object. A Blueprint is a way to organize a group of
# related views and other code. Instead of registering views and other code
# directly with an application, they are registered with a blueprint.
# Then, the blueprint is registered with the application when it is available
# in the factory function.
api = Blueprint('api', __name__)

# We import the routes module at the end to avoid circular dependencies.
# The routes module, in turn, will use the 'api' blueprint object defined above.
from . import routes