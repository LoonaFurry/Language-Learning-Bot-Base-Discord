import discord
from discord.ext import commands
import sqlite3

bot = commands.Bot(command_prefix='!')

# Veritabanı bağlantısı
conn = sqlite3.connect('kelimeler.db')
c = conn.cursor()

# Kelime tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS kelimeler
             (kelime text, turkce text)''')
conn.commit()

# Kelime ekleme fonksiyonu
def kelime_ekle(kelime, turkce):
    c.execute("INSERT INTO kelimeler VALUES (?, ?)", (kelime, turkce))
    conn.commit()

# Kelime silme fonksiyonu
def kelime_sil(kelime):
    c.execute("DELETE FROM kelimeler WHERE kelime=?", (kelime,))
    conn.commit()

# Tüm kelimeleri getirme fonksiyonu
def kelimeleri_getir():
    c.execute("SELECT * FROM kelimeler")
    return c.fetchall()

# Kelimenin Türkçe karşılığını getirme fonksiyonu
def turkce_karsiligi_getir(kelime):
    c.execute("SELECT turkce FROM kelimeler WHERE kelime=?", (kelime,))
    return c.fetchone()

# Kelime tahmin etme fonksiyonu
def kelime_tahmin_et(kelime):
    turkce_karsiligi = turkce_karsiligi_getir(kelime)
    if turkce_karsiligi:
        return f"{kelime} kelimesinin Türkçe karşılığı {turkce_karsiligi[0]}."
    else:
        return f"{kelime} kelimesinin Türkçe karşılığı bulunamadı."

# Kelime ekleme komutu
@bot.command()
async def kelimeekle(ctx, kelime: str, turkce: str):
    kelime_ekle(kelime, turkce)
    await ctx.send(f"{kelime} kelimesi başarıyla eklendi.")

# Kelime silme komutu
@bot.command()
async def kelimesil(ctx, kelime: str):
    kelime_sil(kelime)
    await ctx.send(f"{kelime} kelimesi başarıyla silindi.")

# Kelime listesi komutu
@bot.command()
async def kelimeler(ctx):
    kelimeler = kelimeleri_getir()
    if kelimeler:
        kelime_listesi = "\n".join([f"{kelime[0]}: {kelime[1]}" for kelime in kelimeler])
        await ctx.send(f"Kelime listesi:\n{kelime_listesi}")
    else:
        await ctx.send("Kelime listesi boş.")

# Kelime tahmin etme komutu
@bot.command()
async def tahminet(ctx, kelime: str):
    tahmin = kelime_tahmin_et(kelime)
    await ctx.send(tahmin)

bot.run('BOT_TOKEN')