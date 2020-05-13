# Project 3 - Pizza

Web Programming with Python and JavaScript

A pizza ordering ecommerce website build as part of a coursework project of CS50W course based on the specifications mentioned in this page -> https://docs.cs50.net/web/2020/x/projects/3/project3.html


Summary of the directories present:-

Pizzapp is a web application for handling a pizza restaurant’s online orders. Users will be able to browse the restaurant’s menu, add items to their cart, make payment and submit their orders. Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed.

pizza - project directory of the app

menu - menu app defines the DB table schema for the products and their categories which are part of the menu, and rendering template with their info and form for the user to add the product present into their cart.

users - users app manages the registration, authentication, authorization, login and logout aspects of the app.

cart - cart app handles all cart items data related processing, and saving the cart items pertaining to a user across sessions until a order is placed, after which the cart is reset to 0.

orders - order app defines the DB table schema for the orders and the order items selected by the customer with their quantity and other related info. It also handles the checkout process that includes accepting the address, making payment and placing the order, after which the user will receive an email confirming the order.


A video demo of the project -> 
