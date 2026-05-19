# SUBSISTEM 1: Sistem Suara (AudioSystem)
class AudioSystem:
    def __init__(self):
        self.volumeLevel: int = 0

    def playMusic(self) -> None:
        print("AudioSystem: Memutar musik latar belakang...")

    def setVolume(self, level: int) -> None:
        self.volumeLevel = level
        print(f"AudioSystem: Mengubah tingkat volume ke {self.volumeLevel}%")

    def setSurroundSound(self) -> None:
        print("AudioSystem: Mengaktifkan mode efek suara Surround 5.1!")

    def stop(self) -> None:
        print("AudioSystem: Menghentikan seluruh output suara.")


# SUBSISTEM 2: Sistem Layar/Proyektor (VideoSystem)
class VideoSystem:
    def powerOn(self) -> None:
        print("VideoSystem: Menyalakan proyektor dan menurunkan layar...")

    def powerOff(self) -> None:
        print("VideoSystem: Mematikan proyektor dan menggulung layar.")

    def play(self, movieTitle: str) -> None:
        print(f"VideoSystem: Memulai pemutaran film -> '{movieTitle}'")

    def pause(self) -> None:
        print("VideoSystem: Menunda (pause) pemutaran film.")


# SUBSISTEM 3: Sistem Lampu Ruangan (LightSystem)
class LightSystem:
    def __init__(self):
        self.brightnessLevel: int = 100  

    def turnOn(self) -> None:
        self.brightnessLevel = 100
        print("LightSystem: Lampu utama dinyalakan (Kecerahan 100%).")

    def turnOff(self) -> None:
        self.brightnessLevel = 0
        print("LightSystem: Lampu utama dimatikan total (0%).")

    def dim(self, level: int) -> None:
        self.brightnessLevel = level
        print(f"LightSystem: Merendahkan tingkat cahaya ke {self.brightnessLevel}%.")


# KELAS UTAMA: Home Theater Facade
class HomeTheaterFacade:
    def __init__(self, audio: AudioSystem, video: VideoSystem, light: LightSystem):
        # Menyimpan referensi subsistem sebagai atribut private (-)
        self._audio: AudioSystem = audio
        self._video: VideoSystem = video
        self._light: LightSystem = light

    def watch_movie(self, movie_name: str) -> None:
        print(f"\n--- MENYIAPKAN SKENARIO NONTON FILM: {movie_name.upper()} ---")        
        self._light.dim(20)                      
        self._audio.setVolume(50)                
        self._audio.setSurroundSound()            
        self._video.powerOn()                    
        self._video.play(movie_name)             
        
        print("--- BIOSKOP RUMAH SIAP, SELAMAT MENONTON! ---\n")


# CODE CLIENT: Simulasi Eksekusi Program
if __name__ == "__main__":
    komponen_audio = AudioSystem()
    komponen_video = VideoSystem()
    komponen_light = LightSystem()

    bioskop_mini = HomeTheaterFacade(komponen_audio, komponen_video, komponen_light)

    bioskop_mini.watch_movie("Interstellar")