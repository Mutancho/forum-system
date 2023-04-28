# Forum System


## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/AntonNikiforov/forum_system/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

## Name
Forum System

## Description
Forum System is an intuitive and robust Python-based backend application that powers online forum services. Developed with FastAPI and SQL (MariaDB), it offers a comprehensive suite of features that allows users to create topics, post replies, and engage in dynamic discussions. It also includes advanced administrative capabilities such as locking/unlocking topics, setting the best replies, and managing user roles and categories. Secure user registration and authentication are facilitated through JWT. With its blend of technology and user-centric design, Forum System is equipped to deliver a seamless and engaging online forum experience.

## Installation
List Of Technologies:
Python
FastAPI
SQL (MariaDB)
Pydantic
JWT for authentication

To install required modules use "pip install –r requirements.txt" in ternimal.

## Visuals
MariaDB relational database diagram:
![Alt text](/images/database_diagram.jpg)


## Usage
The HTTP endpoints are listed in http://127.0.0.1:8000/docs 

Refer to docstrings and typehints if you have questions regarding certain functionality.

To run the project first include a .env in config folder with the following parameters:

DATABASE_HOSTNAME
DATABASE_PORT
DATABASE_PASSWORD
DATABASE_NAME
DATABASE_USERNAME 
SECRET_KEY
ALGORITHM= eg. "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="enter integer for minutes"

When you provide an authorization token go to the authorisation tab in postman and there you should select bearer token, enclosed in quotation marks. 


## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.


## Authors and acknowledgment
We want to thank our lecturers and colleagues at Telerik Academy for the continous support throughtout the integration of the project. 

## License
Telerik Academy

