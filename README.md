## Favorite things
[![Coverage Status](https://coveralls.io/repos/github/omobosteven/favorite-things/badge.svg?branch=develop)](https://coveralls.io/github/omobosteven/favorite-things?branch=develop)
[![Build Status](https://travis-ci.com/omobosteven/favorite-things.svg?branch=develop)](https://travis-ci.com/omobosteven/favorite-things)

An application that allows users to track their favorite things based on category and ranking

## Content
- [Development Set Up](#development-set-up)
  * [Backend](#backend)
  * [Frontend](#frontend)
- [Deployment Steps](#deployment-steps-on-aws)
- [API endpoints](#api-endpoints)
- [Technologies Used](#built-with)

## Development set up

#### (BACKEND)

- Check that python 3.7, pip, pipenv and postgres are installed on your machine.

- Clone the repo and cd into it
    ```
    git clone https://github.com/omobosteven/favorite-things
    ``` 
 - Install dependencies
    ```
    make pipenv-install
    ```
 - Create Application environment variables and save them in .env file
    ```
	  SECRET_KEY='djangosettingssecretkey'
	  DB_NAME='database_name'
	  DB_PASS='database_password'
	  DB_USER='database_user'
	  DB_HOST='127.0.0.1'
	  DB_PORT='port'
    ```
    
  - Run migrations
  	```
  	make migrate
	```
	
- Run application
    ```
    make start
    ```
    
- Running Tests
 - To run tests, observe test coverage and check for flake8 errors. Run the command below.
	 ```
	 make test
	 ```
 - To obtain html browser report. Run command below:
	 ```
	 make html-test-coverage
	 ```
	 ```
	  A folder titled htmlcov will be generated. Open it and copy the path  of index.html and paste it in your browser.
	 ```

#### (FRONTEND)
- Check that Node (recommended v11.12+) and npm are installed on your machine.

- Install dependencies
```
make npm-install
```

- Before running the below commands ensure to cd into the client directory and create environment variables and save them in .env.development file
```
VUE_APP_AXIOS_BASE_URL='http://127.0.0.1:8000/'
```
```
This application uses the browser's cookie for authentication, ensure the base url matches the url you're using for the frontend.
```
- Compiles and hot-reloads for development
```
make serve-client
```

- Compiles and minifies for production
```
make build-client
```

- Open Application in browser
```
http://127.0.0.1:8080
```

- NB: You can choose to create a django admin superuser and create categories using the superuser. These categories will serve as the default categories for the every user.

## Deployment steps on AWS
- Go to [AWS](https://aws.amazon.com/) and create an EC2 instance using Ubuntu Server 18.04 LTS (HVM), SSD Volume Type 64-bit x86. NB: Ensure to Download the key pair generated
- Go to security groups under network and security on AWS console and enable the following ports [8000, 80] source should be set to anywhere.
- On your machine navigate to the directory where the key_pair was saved.
- Set the file permission of your private key_pair
	```
	sudo chmod 400 key_pair.pem
	```
- SSH to the server, copy your "IPv4 Public IP" from the EC2 instance on AWS console
	```
	ssh -i testing.pem ubuntu@your_public_ip_address
	```
- Clone the repo and cd into it
    ```
    git clone https://github.com/omobosteven/favorite-things
    ``` 
- Create Application environment variables and save them in .env file
    ```
	  SECRET_KEY='djangosettingssecretkey'
	  DB_NAME='database_name'
	  DB_PASS='database_password'
	  DB_USER='database_user'
	  DB_HOST='127.0.0.1'
	  DB_PORT='port'
    ```
- cd into the client directory and create environment variables and save them in .env.production file
```
VUE_APP_AXIOS_BASE_URL='http://your_Public_DNS_(IPv4)_on_AWS_console:8000/'
```
e.g
```
VUE_APP_AXIOS_BASE_URL='http://ec2-3-18-220-65.us-east-2.compute.amazonaws.com:8000/'
```
- Ensure you are in the favorite thing directory and create a file `favorite-things`, copy and edit the block of code below
```
server {
    listen      80;
    server_name {{ Public IP }}; 
    server_name {{ Public DNS  }};
    charset utf-8;
    root    /home/ubuntu/favorite-things/client/dist;
    index   index.html index.htm;
    # Always serve index.html for any request
    location / {
        root /home/ubuntu/favorite-things/client/dist;
        try_files $uri /index.html;
    }
    error_log  /var/log/nginx/vue-app-error.log;
    access_log /var/log/nginx/vue-app-access.log;
}
```
- Set the file permission of the deployment script file
	```
	sudo chmod 774 description.sh
	```
	
- Run the deployment script
	```
	./deployment.sh
	```
	
- Open app on browser with your Public DNS (IPv4) on AWS console


## API Endpoints
<table>
  <tr>
      <th>Request</th>
      <th>End Point</th>
      <th>Action</th>
  </tr>
    <tr>
      <td>POST</td>
      <td>/users/register</td>
      <td>Register a User</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/users/login</td>
    <td>Login a user</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/categories</td>
    <td>Get all default and user's categories</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/categories</td>
    <td>Create a new category</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/thing</td>
    <td>Create a favorite thing</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/things</td>
    <td>Get all favorite things</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/things/{int:id}</td>
    <td>Get the details of a favorite thing</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/thing/categories/{int:category_id}</td>
    <td>Get all favorite thing in category</td>
  </tr>
  <tr>
    <td>PUT</td>
    <td>/thing/{int:id}</td>
    <td>Update a favorite thing</td>
  </tr>  
  <tr>
    <td>PATCH</td>
    <td>/thing/{int:id}</td>
    <td>Update a favorite thing</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/logs</td>
    <td>Get audit log for user</td>
  </tr>
</table>


## Built with
- Python version 3.7
- Django
- Django REST Framework
- VueJs
- Postgres
