import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import discord
from datetime import datetime, timedelta  # Zaman işlemleri için gerekli sınıflar

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.pokemon_hp = random.randint(200, 400)
        self.pokemon_power = random.randint(30, 60)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon sağliği geri yüklenir. Mevcut sağlik: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz: {current_time+delta_time}"          

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['sprites']['front_default']  #  Pokémon görüntüsünün URL'sini döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"Pokémonunuzun ismi: {self.name}"  # Pokémon adını içeren dizeyi döndürür

        if not self.pokemon_hp:
            self.pokemon_hp = await self.get_hp()  # Henüz atanmamışsa bir HP değeri atama
        return f"Pokémonunuzun HP'si: {self.pokemon_hp}"  # Pokémon HP'sini içeren dizeyi döndürür

        if not self.pokemon_power:
            self.pokemon_power = await self.get_power()  # Henüz atanmamışsa bir güç değeri atama
        return f"Pokémonunuzun gücü: {self.pokemon_power}"  # Pokémon gücünü içeren dizeyi döndürür

        
        return f"Pokémon'un türü: {self.__class__.__name__}"

    async def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

 


    async def show_img(self):
         # PokeAPI aracılığıyla bir pokémonun görüntüsünün URL'sini almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['sprites']['front_default']  #  Pokémon görüntüsünün URL'sini döndürme
                else:
                    return None  # İstek başarısız olursa varsayılan adı döndürür

class Wizard(Pokemon):
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Düşmanın Wizard veri tipi olup olmadığının kontrol edilmesi (Sihirbaz sınıfının bir örneği midir?) 
            chance = random.randint(1, 5) 
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanildi!"
        return await super().attack(enemy)
    async def feed(self):
        return await super().feed(feed_interval=10)  
class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)  
        self.pokemon_power += super_power
        result = await super().attack(enemy)  
        self.pokemon_power -= super_power
        return result + f"\nDövüşçü Pokémon süper saldiri kullandi. Eklenen güç: {super_power}"
    async def feed(self):
        return await super().feed(hp_increase=20)