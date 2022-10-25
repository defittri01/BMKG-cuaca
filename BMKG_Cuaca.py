#author Defit Tri H.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os, glob, cv2, time, sys, urllib.request, random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

class BMKGCuaca():
  def __init__(self):
    sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    # chrome_options.headless = False
    # chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--no-sandbox')

    self.driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=chrome_options)

    try:
      self.driver.get('https://dataonline.bmkg.go.id/home')
      self.driver.save_screenshot('bmkg_login.png')
      print('chrome is opened successfully')
    except:
      print('failed to open chrome browser')

  def login(self, email, password):  
    email_box = self.driver.find_element("xpath", '/html/body/div[2]/div/div/div/div[1]/div[1]/div/form[1]/div[1]/div/input')
    email_box.clear()
    email_box.send_keys(email)

    password_box = self.driver.find_element("xpath", '/html/body/div[2]/div/div/div/div[1]/div[1]/div/form[1]/div[2]/div/input')
    password_box.clear()
    password_box.send_keys(password)

    self.display_login_capt()

  def display_login_capt(self):
    now_dir = os.getcwd()
    captcha = self.driver.find_element("xpath", '//*[@id="capimage"]/img')
    captcha_url = captcha.get_attribute('src')
    urllib.request.urlretrieve(captcha_url, 'captcha_img.jpg')
    captcha_img = cv2.imread(now_dir+'/captcha_img.jpg')
    plt.imshow(captcha_img)

  def solve_login_capt(self):
    captcha = input ("solve captcha: ")

    captcha_box = self.driver.find_element("xpath", '//*[@id="captcha"]')
    captcha_box.clear()
    captcha_box.send_keys(captcha)

    password_box = self.driver.find_element("xpath", '/html/body/div[2]/div/div/div/div[1]/div[1]/div/form[1]/div[2]/div/input')
    password_box.send_keys(Keys.RETURN)

    try:
      WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div/div/h1')))
      print('Login success')

    except:
      print('Login failed, try again ...')

  def set_parameter(self, provinsi, stasiun):
    self.driver.get('https://dataonline.bmkg.go.id/data_iklim')

    but_stasiun = self.driver.find_element("xpath", '/html/body/div[2]/div[2]/div[3]/div/div/div[1]/div[2]/div/div[2]/form/div[1]/span/span[1]/span/span[1]')
    but_stasiun.click()
    box_stasiun = self.driver.find_element("xpath", '/html/body/span/span/span[1]/input')
    box_stasiun.send_keys('UPT')
    box_stasiun.send_keys(Keys.RETURN)
    print('Jenis stasiun: UPT')

    print('Parameter dipilih: Curah hujan (RR)')
    opt_RR = self.driver.find_element("xpath", '//*[@id="form"]/div[2]/div/div/div[2]/div[3]/input')
    opt_RR.click()

    print('Parameter dipilih: Kecepatan angin rata-rata (ff_avg)')
    opt_ff_avg = self.driver.find_element("xpath", '//*[@id="form"]/div[2]/div/div/div[2]/div[5]/input')
    opt_ff_avg.click()

    print('Parameter dipilih: Kelembaban rata-rata (RH_avg)')
    opt_RH_avg = self.driver.find_element("xpath", '//*[@id="form"]/div[2]/div/div/div[2]/div[6]/input')
    opt_RH_avg.click()

    print('Parameter dipilih: Lamanya penyinaran matahari (ss)')
    opt_ss = self.driver.find_element("xpath", '//*[@id="form"]/div[2]/div/div/div[2]/div[7]/input')
    opt_ss.click()

    print('Parameter dipilih: Temperatur rata-rata (T_avg)')
    opt_Tavg = self.driver.find_element("xpath", '//*[@id="form"]/div[2]/div/div/div[2]/div[10]/input')
    opt_Tavg.click()

    print(f'Provinsi: {provinsi}'.format(provinsi))
    but_provinsi = self.driver.find_element("xpath", '//*[@id="select2-idrefprovince-container"]')
    but_provinsi.click()
    box_provinsi = self.driver.find_element("xpath", '/html/body/span/span/span[1]/input')
    box_provinsi.send_keys(provinsi)
    box_provinsi.send_keys(Keys.RETURN)

    print(f'No/Nama Stasiun: {stasiun}'.format(stasiun))
    but_sta = self.driver.find_element("xpath", '/html/body/div[2]/div[2]/div[3]/div/div/div[1]/div[2]/div/div[2]/form/div[5]/span/span[1]/span/span[1]')
    but_sta.click()
    box_sta = self.driver.find_element("xpath", '/html/body/span/span/span[1]/input')
    box_sta.send_keys(stasiun)
    time.sleep(1)
    box_sta.send_keys(Keys.DOWN)
    box_sta.send_keys(Keys.RETURN)

  def from_to_date(self, date_start, date_end):
    box_from = self.driver.find_element("xpath", '//*[@id="from"]')
    box_from.clear()
    box_from.send_keys(date_start)

    box_to = self.driver.find_element("xpath", '//*[@id="to"]')
    box_to.clear()
    box_to.send_keys(date_end)

    self.driver.find_element("xpath", '//body').click()

    but_proses = self.driver.find_element("xpath", '//*[@id="form"]/div[7]/div/div/button/span[1]')
    but_proses.click()

  def click_star(self):
    # prints a random value from the list
    list1 = [1, 2, 3, 4, 5]

    for i in range(1,5):
      star_num = random.choice(list1)
      # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="form-feedback"]/div[{i}]/div/div[1]/ul/a[{star_num}]'.format(i,star_num))))
      # but_star = self.driver.find_element("xpath", f'//*[@id="form-feedback"]/div[{i}]/div/div[1]/ul/a[{star_num}]'.format(i,star_num))
      but_star = self.driver.find_element("xpath", f'/html/body/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[3]/form/div[{i}]/div/div[1]/ul/a[{star_num}]'.format(i,star_num))
      
      self.driver.find_element("xpath", '//body').click()
      but_star.click()

    but_kirim = self.driver.find_element("xpath", '//*[@id="form-feedback"]/div[6]/div/button')
    but_kirim.click()

  def click_download(self):
    but_download = self.driver.find_element("xpath", '//*[@id="form-download"]/button[1]')
    but_download.click()

  def rename_file(self, tahun, new_name):
    now_dir = os.getcwd()
    Path(now_dir+tahun).mkdir(parents=True, exist_ok=True)

    while True:
      files_name = sorted(glob.glob(now_dir + '/*.xlsx'), key=os.path.getmtime,reverse=True)
      target = now_dir + '/laporan_iklim_harian.xlsx'

      if target in files_name:
          # print(target)
          old_path = files_name[0]
          path = old_path.split("/")
          new_path = os.path.join(path[0], tahun , new_name + '.xlsx')
          # print(old_path, new_path)
          os.rename(old_path, new_path)
          
          break


