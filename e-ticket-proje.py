import datetime

from functools import wraps

# Kullanıcı ve admin bilgileri
users = {}
admins = {"irfan": "irfan123", "veysel": "veysel123"}


# Ticket sınıfı
class Ticket:
    ticketlist = []

    def __init__(self, activity, time, price, stock):
        self.activity = activity
        self.time = time
        self.price = price
        self.stock = stock
        self.initial_stock = stock
        Ticket.ticketlist.append(self)  # Ticketlistnin genişliğini arttırmak için.


# Bu decorator, yalnızca adminlerin belirli işlemleri yapmasına izin verir.
# Eğer kullanıcı admin değilse bir uyarı verir.

def admin_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not isinstance(self, Admin):
            print("You do not have the required permissions to perform this action.")
            return None  # İşlem yapılmaz
        return func(self, *args, **kwargs)

    return wrapper


# User sınıfı
class User:
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.tickets = []

    def search_ticket(self):  # ticketlistteki aktivitelerinin kullanıcı tarafından aranıp bulunması için.
        activity = input("Please write your activity that you want to go: ")
        for t in Ticket.ticketlist:
            if t.activity == activity:
                print(f"Activity: {t.activity}, Time: {t.time}, Price: {t.price}, Stock: {t.stock}")
                return
        print("We cannot find the activity that you want")

    def buy_ticket(self):  # Kullanıcının ticket satın alması için
        activity = input("Please write your activity that you want to buy a ticket: ")
        for t in Ticket.ticketlist:
            if t.activity == activity and t.stock > 0:
                self.tickets.append(t)
                t.stock -= 1
                print(f"Ticket for {t.activity} purchased!")
                return
        print("Ticket not available or sold out!")

    def del_ticket(self):  # Kullanıcının aldığı bileti iptal edebilmesi için
        activity = input("Please write your activity that you want to cancel: ")
        for t in self.tickets:
            if t.activity == activity:
                self.tickets.remove(t)
                t.stock += 1
                print(f"Ticket for {t.activity} canceled!")
                return
        print("You don't have any ticket for this event!")

    def change_password(self):  # Kullanıcının şifresini değiştirebilmesi için
        old_password = input("Please write your current password: ")
        if self.password == old_password:
            new_password = input("Please write your new password: ")
            self.password = new_password
            print("Password changed!")
            return
        else:
            print("Invalid password!")


# Admin classı oluşturup bu e-ticket sitesindeki aktiviteleri sadece adminin yönetmesi ve adminin aktivitelerin satış raporlarına bakması için(User classından inherit alıyor)
class Admin(User):
    @admin_required  # Admin yetkisi kontrol ediliyor
    def define_ticket(self):  # Aktivite tanımlamak için
        activity = input("Enter the activity name: ")
        time_str = input("Enter time (YYYY-MM-DD HH:MM): ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock: "))
        time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        Ticket(activity, time, price, stock)
        print(f"Ticket for {activity} created!")

    @admin_required  # Admin yetkisi kontrol ediliyor
    def sales_report(self):  # Satış Raporlarını görebilmek için
        print("Sales Report:")
        for ticket in Ticket.ticketlist:
            sold = ticket.initial_stock - ticket.stock
            print(f"Activity: {ticket.activity}, Sold: {sold}, Available: {ticket.stock}")

    @admin_required  # Admin yetkisi kontrol ediliyor
    def add_admin(self):  # Siteye yeni adminler ekleyebilmek için
        id = input("Username: ")
        password = input("Password: ")
        if id not in admins:
            admins[id] = password
            print(f"{id} admin created successfully!")


# Giriş fonksiyonu
def login():
    while True:

        print("1 for Login")

        print("2 for Register")

        print("3 for Shutting down")

        choice = int(input("Choose an option: "))

        if choice == 1:

            id = input("Username: ")

            password = input("Password: ")

            if id in admins and admins[id] == password:  # Kontrollerin sağlandığı kısım

                print(f"Welcome Admin {id}!")
                admin_user = Admin(id, password)
                main_menu(admin_user)
                break

            elif id in users and users[id].password == password:

                print(f"Welcome {id}!")

                return main_menu(users[id])

            else:

                print("Invalid username or password!")

        elif choice == 2:

            id = input("Username: ")

            password = input("Password: ")

            if id not in users:

                users[id] = User(id, password)

                print("Account created successfully!")

            else:

                print("Username already exists!")

        elif choice == 3:

            print("Shutting down...")

            break

        else:

            print("Invalid choice!")


def main_menu(user):  # Siteye giriş yapıldıktan sonra kullanıcının çeşitli etkinlikleri yapabileceği arayüz
    while True:

        print("\nMain Menu:")

        print("1 for Buy Ticket")

        print("2 for Cancel Ticket")

        print("3 for Search Ticket")

        print("4 for Change Password")

        print("5 for Logout")

        if isinstance(user, Admin):
            print("6 for Define Ticket")

            print("7 for Sales Report")

            print("8 for Add An Admin")

        choice = int(input("Choose an option: "))

        if choice == 1:

            user.buy_ticket()

        elif choice == 2:

            user.del_ticket()

        elif choice == 3:

            user.search_ticket()

        elif choice == 4:

            user.change_password()

        elif choice == 5:

            print("Logging out...")
            return login()

        elif isinstance(user, Admin):

            if choice == 6:

                user.define_ticket()

            elif choice == 7:

                user.sales_report()

            elif choice == 8:

                user.add_admin()

        else:

            print("Invalid choice!")


# Programı başlatma
print("Welcome to E-Ticket Sale Application")

user = login()

if user:
    main_menu(user)