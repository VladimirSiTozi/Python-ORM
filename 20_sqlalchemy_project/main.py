import random

from sqlalchemy.orm import sessionmaker
from models import Employee, City, engine


# CREATE
# Session = sessionmaker(bind=engine)
# with Session() as session:
#     employee = Employee(
#         first_name='John',
#         last_name='Smith',
#         age=34
#     )
#     session.add(employee)
#     session.commit()

# CREATE
# The id is not necessary
# Session = sessionmaker(bind=engine)
# with Session() as session:
#     data = [
#         {"id":1,"first_name":"Cordi","last_name":"Spelling","age":39},
#         {"id":2,"first_name":"Kean","last_name":"Laurence","age":60},
#         {"id":3,"first_name":"Sheilakathryn","last_name":"Veelers","age":54},
#         {"id":4,"first_name":"Hammad","last_name":"Maith","age":23},
#         {"id":5,"first_name":"Sile","last_name":"Frye","age":50},
#         {"id":6,"first_name":"Maurizio","last_name":"Williamson","age":73},
#         {"id":7,"first_name":"Nikki","last_name":"Blockley","age":34},
#         {"id":8,"first_name":"Jenine","last_name":"Fiddymont","age":32},
#         {"id":9,"first_name":"Ingaborg","last_name":"Dales","age":25},
#         {"id":10,"first_name":"Edik","last_name":"Doull","age":62},
#         {"id":11,"first_name":"Bevvy","last_name":"Isakovitch","age":22},
#         {"id":12,"first_name":"Dalila","last_name":"Walter","age":33},
#         {"id":13,"first_name":"Washington","last_name":"Richardet","age":80},
#         {"id":14,"first_name":"Efrem","last_name":"Borrows","age":66},
#         {"id":15,"first_name":"Morna","last_name":"Mantha","age":58},
#         {"id":16,"first_name":"Hersh","last_name":"Santos","age":61},
#         {"id":17,"first_name":"Jillayne","last_name":"Couvert","age":38},
#         {"id":18,"first_name":"Lyndell","last_name":"Tower","age":58},
#         {"id":19,"first_name":"Analiese","last_name":"Butler-Bowdon","age":19},
#         {"id":20,"first_name":"Winonah","last_name":"Maynard","age":46},
#         {"id":21,"first_name":"Anson","last_name":"Ovens","age":32},
#         {"id":22,"first_name":"Ursuline","last_name":"Gosart","age":39},
#         {"id":23,"first_name":"Cullin","last_name":"Seydlitz","age":75},
#         {"id":24,"first_name":"Miquela","last_name":"Edney","age":77},
#         {"id":25,"first_name":"Chane","last_name":"Blaxter","age":29},
#         {"id":26,"first_name":"Roland","last_name":"Alexsandrowicz","age":80},
#         {"id":27,"first_name":"Esme","last_name":"Oxburgh","age":37},
#         {"id":28,"first_name":"Emalia","last_name":"Olliff","age":39},
#         {"id":29,"first_name":"Lorrin","last_name":"Hansard","age":63},
#         {"id":30,"first_name":"Nichols","last_name":"Redmond","age":37},
#         {"id":31,"first_name":"Katrinka","last_name":"Kilduff","age":36},
#         {"id":32,"first_name":"Darcee","last_name":"McCorley","age":70},
#         {"id":33,"first_name":"Daune","last_name":"Carn","age":79},
#         {"id":34,"first_name":"Derby","last_name":"Pomroy","age":74},
#         {"id":35,"first_name":"Noe","last_name":"Binder","age":24},
#         {"id":36,"first_name":"Rosemary","last_name":"Battison","age":50},
#         {"id":37,"first_name":"Emelita","last_name":"McKellen","age":66},
#         {"id":38,"first_name":"Dulcie","last_name":"Vaney","age":52},
#         {"id":39,"first_name":"Fredek","last_name":"Durham","age":51},
#         {"id":40,"first_name":"Debera","last_name":"Leftbridge","age":40},
#         {"id":41,"first_name":"Cristal","last_name":"Esland","age":80},
#         {"id":42,"first_name":"Johnnie","last_name":"Negal","age":63},
#         {"id":43,"first_name":"Griffin","last_name":"Szreter","age":63},
#         {"id":44,"first_name":"Ertha","last_name":"Wale","age":46},
#         {"id":45,"first_name":"Sandy","last_name":"Aubri","age":19},
#         {"id":46,"first_name":"Odilia","last_name":"Hembrow","age":45},
#         {"id":47,"first_name":"Tonia","last_name":"Callway","age":72},
#         {"id":48,"first_name":"Tucky","last_name":"Gorrie","age":38},
#         {"id":49,"first_name":"Skye","last_name":"Pellington","age":19},
#         {"id":50,"first_name":"Cozmo","last_name":"Bramwich","age":58},
#         {"id":51,"first_name":"Haley","last_name":"Sinkins","age":79},
#         {"id":52,"first_name":"Ethelbert","last_name":"Hammett","age":22},
#         {"id":53,"first_name":"Ree","last_name":"Camplejohn","age":30},
#         {"id":54,"first_name":"Kerby","last_name":"Ellicock","age":45},
#         {"id":55,"first_name":"Maxi","last_name":"Winterbottom","age":26},
#         {"id":56,"first_name":"Ettie","last_name":"Rowlstone","age":18},
#         {"id":57,"first_name":"Andeee","last_name":"Middleweek","age":53},
#         {"id":58,"first_name":"Stephannie","last_name":"Slany","age":30},
#         {"id":59,"first_name":"Bartram","last_name":"Engledow","age":51},
#         {"id":60,"first_name":"Whitney","last_name":"Carlozzi","age":34},
#         {"id":61,"first_name":"Lucienne","last_name":"Enston","age":40},
#         {"id":62,"first_name":"Sarge","last_name":"Doale","age":67},
#         {"id":63,"first_name":"Marsiella","last_name":"Castagna","age":33},
#         {"id":64,"first_name":"Hatty","last_name":"Cersey","age":60},
#         {"id":65,"first_name":"Gavra","last_name":"Bartosek","age":73},
#         {"id":66,"first_name":"Cyrus","last_name":"Chalmers","age":34},
#         {"id":67,"first_name":"Bertine","last_name":"Ketts","age":76},
#         {"id":68,"first_name":"Chandal","last_name":"Roof","age":75},
#         {"id":69,"first_name":"Felicdad","last_name":"Layland","age":57},
#         {"id":70,"first_name":"Lorry","last_name":"Duligal","age":30},
#         {"id":71,"first_name":"Edwina","last_name":"Iddison","age":47},
#         {"id":72,"first_name":"Lucky","last_name":"Metrick","age":78},
#         {"id":73,"first_name":"Abbott","last_name":"Winney","age":50},
#         {"id":74,"first_name":"Aleen","last_name":"Eddoes","age":34},
#         {"id":75,"first_name":"Bo","last_name":"Gounot","age":75},
#         {"id":76,"first_name":"Marquita","last_name":"Brangan","age":67},
#         {"id":77,"first_name":"Camile","last_name":"Bloxsome","age":20},
#         {"id":78,"first_name":"Adrian","last_name":"Willingale","age":61},
#         {"id":79,"first_name":"Felizio","last_name":"Tibbetts","age":29},
#         {"id":80,"first_name":"Elwira","last_name":"Tromans","age":20},
#         {"id":81,"first_name":"Orv","last_name":"Trighton","age":34},
#         {"id":82,"first_name":"Cy","last_name":"Trustey","age":37},
#         {"id":83,"first_name":"Vladamir","last_name":"Alden","age":28},
#         {"id":84,"first_name":"Fremont","last_name":"Alywen","age":45},
#         {"id":85,"first_name":"Daisey","last_name":"Arpe","age":48},
#         {"id":86,"first_name":"Grissel","last_name":"Jacobowitz","age":55},
#         {"id":87,"first_name":"Cob","last_name":"Amberson","age":22},
#         {"id":88,"first_name":"Onfre","last_name":"Pirie","age":60},
#         {"id":89,"first_name":"Gail","last_name":"Miles","age":21},
#         {"id":90,"first_name":"Eileen","last_name":"Windross","age":44},
#         {"id":91,"first_name":"Charisse","last_name":"Robertshaw","age":28},
#         {"id":92,"first_name":"Ossie","last_name":"Borton","age":33},
#         {"id":93,"first_name":"Selie","last_name":"Flippen","age":70},
#         {"id":94,"first_name":"Maud","last_name":"Storms","age":32},
#         {"id":95,"first_name":"Brooke","last_name":"Huddy","age":60},
#         {"id":96,"first_name":"Rosalinda","last_name":"Mazella","age":26},
#         {"id":97,"first_name":"Brodie","last_name":"Schuck","age":18},
#         {"id":98,"first_name":"Carri","last_name":"Ridsdole","age":71},
#         {"id":99,"first_name":"Demetre","last_name":"Rankmore","age":67},
#         {"id":100,"first_name":"Amy","last_name":"Sturdey","age":68}
#     ]
#
#     for d in data:
#         employee = Employee(
#             first_name=d['first_name'],
#             last_name=d['last_name'],
#             age=d['age']
#         )
#         session.add(employee)
#     session.commit()


# READ
# Session = sessionmaker(bind=engine)
# with Session() as session:
#     employees = session.query(Employee).all()
#     for e in employees:
#         print(e.first_name, e.last_name, e.age)

# Session = sessionmaker(bind=engine)
# with Session() as session:
#     # employees = session.query(Employee).filter_by(age=40).order_by(Employee.first_name)
#     employees = session.query(Employee).filter(Employee.age >= 40).order_by(Employee.first_name.desc())
#     # employees = session.query(Employee).where(Employee.age >= 40)
#     # employees = session.query(Employee).where(Employee.first_name.startswith('A'))
#     # employees = session.query(Employee).where(Employee.first_name.startswith('A')) | (Employee.age > 60)
#     for e in employees:
#         print(e.first_name, e.last_name, e.age)


# # UPDATE
# Session = sessionmaker(bind=engine)
# with Session() as session:
#     employee = session.query(Employee).first()
#     employee.first_name = 'Metodi'
#     session.commit()

# # DELETE
# Session = sessionmaker(bind=engine)
# with Session() as session:
#     employee = session.query(Employee).first()
#     session.delete(employee)
#     session.commit()


# CREATE
# Session = sessionmaker(bind=engine)
# with Session() as session:
#     session.add_all((
#         City(name='Sofia'),
#         City(name='Plovdiv'),
#         City(name='Varna'),
#         City(name='Burgas'),
#         City(name='Pleven'),
#         City(name='Stara Zagova'),
#         City(name='Vidin'),
#         City(name='Blagoevgrad')
#     ))
#     session.commit()


# Populate city_id in employees
# Session = sessionmaker(bind=engine)
# with Session() as session:
#     employees = session.query(Employee).all()
#     for e in employees:
#         e.city_id = random.randint(1, 8)
#     session.commit()

# Employees From Sofia
# Session = sessionmaker(bind=engine)
# with Session() as session:
#     city = session.query(City).first()
#     for e in city.employees:
#         print(f'{e.first_name} {e.last_name} lives in {city.name}')


# employees - cities
# Session = sessionmaker(bind=engine)
# with Session() as session:
#     city = session.query(City).all()
#     for c in city:
#         for e in c.employees:
#             print(f'{e.first_name} {e.last_name} lives in {c.name}')


# Session = sessionmaker(bind=engine)
# with Session() as session:
#     employees = session.query(Employee).all()
#     for e in employees:
#         print(e.first_name, e.last_name, e.city.name)


