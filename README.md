# Studiosity

## Description

Studiosity is a comprehensive web application designed to support a wide range of study and learning activities. With its robust language support features, it is also ideal for language learners looking to master new languages. Users can create personalized study sets, utilize interactive flashcards, and track their learning progress across various subjects.

## Key Features

1. **Study Set Creation**: Build custom study sets with multimedia support for a diverse learning experience.
2. **Interactive Learning**: Engage with content using interactive tools like flashcards and quizzes.
3. **Language Support**: Benefit from text-to-speech features for language pronunciation and learning.
4. **Progress Tracking**: Keep track of your learning milestones and performance analytics.
5. **Collaborative Learning**: Share and collaborate on study sets with others for group learning sessions.

## Getting Started

To set up Studiosity on your local or remote Ubuntu machine, follow these steps:

1. **Confirm Port Rules**
   - Ensure that your AWS server (or whichever server you use) allows inbound connections from any IP on the following port ranges for TCP: 22, 80, 443.
   - Ensure that your server sends outgoing connections to anywhere.
   - (In AWS, this would be adding rules to the associated security group)
2. **Clone the Studiosity Repository**
   - Clone the repository from GitHub:
     ```
     git clone https://github.com/MGallo-Code/Studiosity.git
     ```
   - Navigate to the cloned directory:
     ```
     cd Studiosity
     ```

3. **Install Docker & Docker-Compose**
   - Follow the official Docker documentation to install Docker and Docker-Compose: [Docker Compose Installation Guide](https://docs.docker.com/compose/install/).
   - Remember to use `sudo` when using `curl` to download docker-compose!
   - Run `sudo chmod +x /usr/local/bin/docker-compose`

4. **Install the Latest Version of Node.js**
   - Install Node.js using NVM (Node Version Manager) by following the instructions here: [NVM Installation Guide](https://nodejs.org/en/download/package-manager/#nvm).

5. **Set Up the Frontend**
   - Navigate to the `frontend` directory within the Studiosity project:
     ```
     cd frontend
     ```
   - Install the necessary npm packages:
     ```
     npm install
     ```
   - Build the frontend assets:
     ```
     npm run build
     ```

6. **Configure Docker Permissions**
   - Add your user to the `docker` group to manage Docker without needing root access:
     ```
     sudo usermod -aG docker ${USER}
     ```
   - Apply the new group membership:
     ```
     newgrp docker
     ```

7. **Check Docker Service**
   - Ensure the Docker service is running properly:
     ```
     sudo systemctl status docker
     ```

8. **Create Your `.env` File**
   - In the main project folder, create a new `.env` file with your environment variables:
     ```
     nano .env
     ```
   - Fill in the `.env` file with your details as shown in the example below:
     ```
     DB_USER=your_postgres_user
     DB_PASSWORD=your_postgres_password
     AWS_ACCESS_KEY_ID=your_aws_access_key_id
     AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
     DJANGO_SECRET_KEY=your_django_secret_key
     SERVER_ADDRESS=your_server_address
     ```
   - Save and exit the editor (in nano, press `Ctrl + X`, then `Y` to confirm, and `Enter` to exit).

9. **Build & Run Docker Container**
   - Run `sudo docker-compose up --build`

10. **Renew/Create Certificate**
   - First, update Studiosity/nginx.conf's `studiosity.io` links to match your website's domain.
   - In the same file, make sure you comment/uncomment any lines specified by comments.
   - Ensure that you renew or create a certificate to access the web page on https:
   ```
   sudo docker-compose exec certbot certbot --webroot --webroot-path=/var/www/certbot -d studiosity.io -d www.studiosity.io --email mgallo.code@gmail.com --agree-tos --no-eff-email certonly
   ```
   - **NOTE!** If having trouble renewing, ensure that the directory `/var/www/certbot/.well-known/acme-challenge/` (as mapped in compose.yml) is somewhere the user has valid access to on the non-container computer.
      - You will probably have to create a directory: `/home/ubuntu/certbot-challenge/.well-known`, or whatever is necessary to match the lines linking to `/var/www/certbot` on the container.
      - /home/ubuntu/certbot-challenge:/var/www/certbot:rw

11. **Set Up AWS Polly (Optional)**
   - If you plan to use AWS Polly for text-to-speech functionality, make sure you have an AWS account.
   - Navigate to the [AWS Management Console](https://aws.amazon.com/console/).
   - Go to the IAM (Identity and Access Management) page and create a new user with programmatic access.
   - Attach the `AmazonPollyFullAccess` policy to the user.
   - Upon creation, you will be provided with the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. Use these for your `.env` file.

After completing these steps, you should have Studiosity set up with all necessary services running. Proceed with the application-specific instructions to start using the application.

## Contributing

We are open to contributions! If you're interested in improving Studiosity, feel free to submit your pull requests or feature suggestions.

## Support

For any questions or issues, please open a ticket on our issue tracker, and we'll be happy to help you out.

Thank you for participating in the Studiosity community, and happy studying!
