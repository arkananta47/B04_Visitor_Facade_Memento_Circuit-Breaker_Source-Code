# SUBSISTEM 1: Manajemen Profil Pengguna
class UserProfile:
    def __init__(self, user_id, name, weight, height, age, activity_factor):
        self.user_id = user_id
        self.name = name
        self.weight = weight  # kilogram
        self.height = height  # centimeter
        self.age = age
        self.activity_factor = activity_factor 

    def calculate_tdee(self):
        # Formula Mifflin-St Jeor untuk menghitung Target Kalori Harian
        bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        tdee = int(bmr * self.activity_factor)
        return tdee


# SUBSISTEM 2: Database Nutrisi Makanan
class FoodDatabase:
    def __init__(self):
        # Data internal hasil kelola Admin (UC-08)
        self._catalog = {
            "Nasi Putih": {"kalori_per_100g": 130, "protein": 2.7},
            "Dada Ayam Panggang": {"kalori_per_100g": 165, "protein": 31.0},
            "Sayur Sop": {"kalori_per_100g": 27, "protein": 1.0},
            "Apel": {"kalori_per_100g": 52, "protein": 0.3}
        }

    def search_food(self, food_name):
        return self._catalog.get(food_name, None)


# SUBSISTEM 3: Food Diary alias Log Tracker
class CalorieTracker:
    def __init__(self):
        self._daily_log = {}

    def add_log(self, user_id, calories_intake):
        if user_id not in self._daily_log:
            self._daily_log[user_id] = 0
        self._daily_log[user_id] += calories_intake

    def get_total_intake(self, user_id):
        return self._daily_log.get(user_id, 0)


# CLASS FACADE: Pintu Masuk Utama Aplikasi EatSmart
class EatSmartAppFacade:
    def __init__(self):
        self.food_db = FoodDatabase()
        self.tracker = CalorieTracker()
        self.users = {
            "1": UserProfile("5025241161", "Aqil", 70, 175, 20, 1.2)
        }

    def get_daily_dashboard_summary(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return "User tidak ditemukan."
        
        target_tdee = user.calculate_tdee()
        total_intake = self.tracker.get_total_intake(user_id)
        remaining_quota = target_tdee - total_intake
        
        return {
            "Nama Pengguna": user.name,
            "Target Kalori (TDEE)": f"{target_tdee} kkal",
            "Kalori yang Dikonsumsi": f"{total_intake} kkal",
            "Sisa Kuota Kalori": f"{remaining_quota} kkal"
        }

    def record_user_meal(self, user_id, food_name, weight_grams):
        print(f"\n[Aksi] Mencatatkan {weight_grams}g {food_name} ke Food Diary...")
        food_item = self.food_db.search_food(food_name)
        
        if not food_item:
            print(f"Peringatan: {food_name} tidak ditemukan di katalog!")
            return False
            
        calories_calculated = int((food_item["kalori_per_100g"] / 100) * weight_grams)
        self.tracker.add_log(user_id, calories_calculated)
        print(f"Sukses: {calories_calculated} kkal ditambahkan ke dalam log harian.")
        return True


# CLIENT CODE: Eksekusi Aplikasi
if __name__ == "__main__":
    eatsmart_system = EatSmartAppFacade()
    target_user_id = "1"

    print("TAMPILAN DASHBOARD AWAL PENGGUNA (uc-01)")
    summary = eatsmart_system.get_daily_dashboard_summary(target_user_id)
    for k, v in summary.items():
        print(f"{k}: {v}")

    # Simulasi user mencatat makanan siang (uc-02)
    eatsmart_system.record_user_meal(target_user_id, "Nasi Putih", 200)
    eatsmart_system.record_user_meal(target_user_id, "Dada Ayam Panggang", 150)

    print("\nTAMPILAN DASHBOARD SETELAH MENCATAT MAKANAN (uc-02/uc-03)")
    updated_summary = eatsmart_system.get_daily_dashboard_summary(target_user_id)
    for k, v in updated_summary.items():
        print(f"{k}: {v}")