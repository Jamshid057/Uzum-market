# JAMSHOP - Oziq-ovqat onlayn do'koni (Flask)

## O'rnatish
1. virtualenv yaratish:
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate      # windows

2. kutubxonalarni o'rnatish:
   pip install -r requirements.txt

3. DB yaratish va seed qilish:
   python seed.py

4. ilovani ishga tushirish:
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run
   yoki: python app.py

## Qisqacha
- Mahsulotni ko‘rish, savatga qo‘shish, savatni ko‘rish va checkout funksiyalari mavjud.
- Keyingi qadamlar: foydalanuvchi autentifikatsiyasi, to‘lov gateway integratsiyasi (PayMe, Click), admin panel, rasm yuklash.
