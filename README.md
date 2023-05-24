### What is this application about?
Create and manage loans for users.

#### POST login
Hit this endpoint with correct credentials to get an authorization token.
User this token for all subsequent APIs to let the application know that it's you.

##### CREATE loan
Hit this endpoint specifying loan amount and tenure. This will create a loan and associated payment schedules.

#### GET loans
Hit this endpoint to see the active loans under your name.

#### PATCH loan
Only admins can hit this endpoint. 
Hit this endpoint to approve a loan. Only when a loan is approved can the users start making payments towards that loan.

#### POST loan/payment
Hit this endpoint specifying the loan & payment schedule towards which you're making the payment. Make sure that amount is greater
than the required payment for this schedule.
If all payment schedules are paid for a particular loan, the loan itself is marked as paid.


## Get started
#### Pre-requisites to run the application
- Docker/Podman
- docker-compose/podman-compose

#### Steps to run the application
- cd to the root of the project
- run `docker-compose up -d`
- verify using `docker ps | grep aspire` you should see two containers running
<!-- blank line -->
<figure class="video_container">
  <iframe src="https://youtu.be/pJBwpx5qvfM" frameborder="0" allowfullscreen="true"> </iframe>
</figure>
<!-- blank line -->


https://github.com/shivamg7/AspireLoans/assets/26554035/a866eb4f-bd39-47ec-a7d2-7a1c0f8201a7




## Assumptions and decision made during development
- A pre-populated list of users is hard-coded in the application. This was done to remove the need for users to create accounts and login
