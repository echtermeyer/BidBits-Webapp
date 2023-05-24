# 🚀 Bidbits - Your Premier Auction Application

Welcome to the **bidbits** repository! This is where we develop and maintain our innovative auction application, designed with a user-friendly UI for seamless selling and bidding experience. This all-in-one application simplifies the auction process; when a user wins a bid, the item is automatically paid for. This repo includes a fully-fledged UI and the capability to directly interact with our database using Adminer.

---

## ⚙️ Getting Started

Start your application in a breeze with our simplified Docker commands. This ensures a uniform setup across different platforms and systems:

1. To build and start the application, run: `docker-compose up --build`

2. To clean everything including volumes: `docker-compose down -v`

---

## 🚪 Access Points & Credentials

Access your application and Adminer using the following ports:

| Port | Description      | URL                                              |
| ---- | ---------------- | ------------------------------------------------ |
| 8051 | Dash Application | [http://localhost:8051/](http://localhost:8051/) |
| 8080 | Adminer          | [http://localhost:8080/](http://localhost:8080/) |

#### Adminer Credentials

To login to Adminer, please use the following credentials:

- **System**: PostgreSQL
- **Server**: db
- **Username**: postgres
- **Password**: postgres
- **Database**: bidbits

> _**Note:** It is highly recommended to change the default credentials before deploying the application in a production environment._

---

## 🙌 Support

If you encounter any issues or have questions regarding the application, please do not hesitate to reach out.

Contact us:

- **David Schäfer**
- **Eric Echtermeyer**

We are here to help and guide you through this process. Happy bidding with **bidbits**!
