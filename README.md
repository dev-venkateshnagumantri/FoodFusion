# OnlineFoodDelivery
<p align="center">
  <img src="https://github.com/dev-venkateshnagumantri/OnlineFoodDelivery/blob/main/static/images/home%20page_m.png" alt="Home" >
  <h2 align="center" style="margin-top: -4px !important;"> Order your favourite food in online from popular restaurants near to you </h2>
</p>

## Introduction:

- Online Food Delivery - FoodOnline is a web application which integrates both car buyers and sellers on one platform.

- The Abstract of the online food delivery web application is it is a platform that connects users with restaurants
and restaurants with users in a single market place. The web application access the user's accurate location and shows
nearby restaurants to the user. The website contains a single smart sign in page which is capable of distinguishing
between customer and vendor and redirects to their respective dashboard.
<p align="center">
  <img src="https://github.com/dev-venkateshnagumantri/OnlineFoodDelivery/blob/main/static/images/customer.png" alt="user" >
</p>
- The website helps the users to know the status of nearby hotels whether open or closed dynamically based on hotel
timings which are updated in real time. It also allows vendors to add their restaurant menu, categories and food items. 
<p align="center">
  <img src="https://github.com/dev-venkateshnagumantri/OnlineFoodDelivery/blob/main/static/images/vendor%201.png" alt="vendor" >
</p>
-  This platform offers International payment
gate way PayPal to ensure a seamless user experience. Overall, the online food delivery web application offers a
convenient and personalized way for users to discover new restaurants and food items.
  
## Purpose:
- The rapid growth of the online food delivery industry has revolutionized the way people order and enjoy their meals.
However, existing food delivery websites often face challenges that hinder the user experience and operational efficiency.
- In response to these challenges, a groundbreaking web application has been developed to address the shortcomings of traditional platforms. It offers a unified platform for vendors and customers, eliminating the need for separate interfaces. Vendors have menu management control to customize their offerings, while customers can rely on accurate restaurant information, including opening hours.
- The application also allows customers to order from multiple restaurants in one transaction, This eliminates the need
for separate orders and potentially reduces delivery fees, providing customers with increased convenience and flexibility.
<p align="center">
  <img src="https://github.com/dev-venkateshnagumantri/OnlineFoodDelivery/blob/main/static/images/foodOnline_Invoice.png" alt="many-many" >
</p>
- Additionally, a popularity-based recommendation system suggests popular dining options based on customers' preferences.
 <p align="center">
  <img src="https://github.com/dev-venkateshnagumantri/OnlineFoodDelivery/blob/main/static/images/Popularity.png" alt="image-popul">
</p>
## About:


I went through building of this web application from scratch by using HTML, CSS, Bootstrap, JavaScript, jQuery and Ajax in Frontend and Django, PostgreSQL, Geo-django and Postgis(Postgres Extension for location related operations) in Backend. The designing of this website took 4 months of time in total.

## Requirements:

run command 

```
pip install -r requirements.txt
```

## Execution:
- You have to ensure that Django and Postgres is successfully installed in your system. 
-	Then Clone this repository using
```
git clone https://github.com/dev-venkateshnagumantri/OnlineFoodDelivery.git
```
**OR**
Zip Download the Repository and Extract it's contents.
-	Now run the [manage.py](https://github.com/dev-venkateshnagumantri/OnlineFoodDelivery/blob/master/manage.py) file
directly in your Terminal using
```
python manage.py runserver 
```
which automatically runs the django server in port 8000

Then, open your browser and type localhost:8000 or 127.0.0.1:8000

- However the Google APIs and PayPal APIs won't work in your system unless yo provide them.
- Be sure to provide your own django secret key and database credentials which can be obtained by creating new django project and new database and thereafter update them in this project.
- you can refer to .env-proto file for what credentials are needed to update here by your own for successful execution of this project.
  
## Feedback:

if you have any feedback do reach me at mail venkateshnagumantri01@gmail.com **OR** at [Linkedin](https://www.linkedin.com/in/venkateshnagumantri)

## License:

[MIT License](License)


<p align='center'><b>Made with ❤ by Venkatesh Nagumantri</b></p>


 








