# Medical_information_systems
Medyczne systemy informacyjne - projekt

19.10.2021 - instalujemy dockera

09.11.2021  - podpinamy baze postgresową
stworzenie klas modeli pacjent i lekarz (django ma wbudowane mechanizmy loginu i hasla)
obługa create get patch delete
walidacja danych, jezeli defniujemy jakies pola to mają byc wymagane przy tworzeniu (serializatory)

Zamodelowanie obsługi użytkowników w systemie:
- użytkownik Pacjent, Lekarz
- wystawienie endpointów do zapisu/odczytu/usunięcia
- walidacja danych


# 16.11.2021 
- upewnienie się, że w projekcie powstają migracje dla modeli wcześniej zdefiniowanych na zajęciach (python manage.py makemigrations, python manage.py migrate)
- upewnienie się że projekt wstaje (python manage.py runserver) i obsługuje komunikacje http
- implementacja obsługi autoryzacji/autentykacji dzięki bibliotece JWT dla Django Rest Framework


# 23.11.2021
- stworzenie specjalizacji - można to zrobić na wiele sposobów, główną opcją musi być łatwe tym zarządzanie, czyli możliwość dodania/usunięcia specjalizacji bez przeładowania aplikacji
obsługa wizyt - musza być podpięte pod specjalizację, zawierać daty, godziny, adresy
umawianie/zapisywanie się na wizytę - tutaj trzeba pamiętać o pozwoleniach np. lekarz mnie może umówić się na swoją lub inną wizytę

# 30.11.2021 
- Stworzyć serwis do wysyłania maili - Django ma gotowe wbudowane mechanizmy
Dodać obsługę tworzenia wyników badań - mogą je wprowadzać tylko lekarze i przypisywać do konkretnych użytkowników
Pacjent może odczytywać tylko swoje wyniki	
Po wprowadzeniu wyników badań, do pacjenta powinien zostać wysłany mail z wynikami

# 07.12.2021 
Zadaniem jest wydzielenie wysyłki maili jako asynchroniczny task

https://docs.celeryproject.org/en/stable/ - dokumentacja Celery
Tutorial do Django + Celery + Redis
https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/
https://www.codingforentrepreneurs.com/blog/celery-redis-django/







#Planowanie:
1. LabCov19;
2. testy covid-19, szczepienia covid-19;
3. Pacjent: imie, nazwisko, wiek, plec, nr. telefonu , mail, czy chce sie szczepic;  
5. Pielegniarka:  ma liste pacjentow, wysyla wyniki mailem;

#Dodatkowe:
1. Platnosc za testy (jesli tego niema to bierzemy ze testy bezplatne) 
2. Rejestracja przez discorda
 
