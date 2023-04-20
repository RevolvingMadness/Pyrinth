# Usage
Here you can find how to use Pyrinth.

## Models
Here are the ways to use models.

### ProjectModel
Here is how you can use the project model to create a project.

```py
from pyrinth import *

user = User.get("RevolvingMadness", "authorization_token")

user.create_project(model)
```

If you dont specify an authorization token when creating the user you will get a `NoAuthorizationError` error.

```py
from pyrinth import *

user = User.get("RevolvingMadness")

user.create_project(model)
```