import os
import time
import argparse
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import glob
def generate_stl(name,name2,height, width, font):
    """
    Hàm tạo file STL từ văn bản nhập vào trên trang text2stl.
    :param name: Nội dung chữ dòng 1 cần tạo STL
    :param name2: Nội dung chữ dòng 2 cần tạo STL
    :param height: Chiều cao chữ
    :param width: Chiều dài chữ
    :param font: Font chữ sử dụng
    """
    print(f"🔨 Đang tạo STL cho dòng 1:'{name}' dòng 2:{name2} với chiều cao {height}mm, chiều dài {width}mm, font: {font}")

    # Cấu hình trình duyệt Chrome headless
    options = Options()
    options.add_argument("--headless")  # Không hiển thị cửa sổ trình duyệt
    driver = webdriver.Chrome(options=options)

    # Mở trang web
    driver.get("https://text2stl.mestres.fr/en-us/generator")
    wait = WebDriverWait(driver, 8)
    driver.refresh()
    time.sleep(4)

    # Tìm phần tử nhập nội dung chữ
    text_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "calcite-text-area[data-test-settings-text]"))
    )
    # Xóa nội dung cũ và nhập nội dung mới
    driver.execute_script("arguments[0].value = '';", text_box)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", text_box)
    text_box.click()  # Click để kích hoạt ô nhập liệu
    text_box.send_keys(Keys.CONTROL, "a")  # Chọn toàn bộ nội dung
    text_box.send_keys(Keys.BACKSPACE)  # Xóa nội dung
    text_box.send_keys(name)  # Nhập nội dung mới
    text_box.send_keys(Keys.ENTER)  # Xóa nội dung
    text_box.send_keys(name2)  # Nhập nội dung mới
    print(f"✅ Đã nhập nội dung: {name} và {name2}")
    driver.execute_script("arguments[0].scrollIntoView();", text_box)
    driver.save_screenshot("ghinoidung.png") 
    time.sleep(1)
    # Nhập kích thước chữ
    text_size_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "calcite-input-number[data-test-settings-size]"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", text_size_input)
    time.sleep(2)
    text_size_input.click()
    text_size_input.send_keys(Keys.CONTROL, "a")  # Chọn toàn bộ nội dung
    text_size_input.send_keys(Keys.BACKSPACE)  # Xóa nội dung
    text_size_input.send_keys(width)  # Nhập giá trị mới

    print(f"✅ Đã đặt chiều dài: {width}mm")
    # Tìm phần tử <img> nhưng click vào phần tử cha của nó
    shape_select = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'img[src="/img/type_1-ef2c7bc83976e176942a0ba5f7e76251.png"]')
        )
    )
    # Cuộn đến phần tử nếu bị che khuất
    driver.execute_script("arguments[0].scrollIntoView();", shape_select)
    time.sleep(1)  # Đợi trang load lại nếu cần

    # Tìm phần tử cha của nó để click (ví dụ: thẻ cha của img)
    parent_element = shape_select.find_element(By.XPATH, "./..")
    driver.execute_script("arguments[0].click();", parent_element)
    text_height_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "calcite-input-number[data-test-settings-height]"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", text_height_input)
    time.sleep(2)
    driver.execute_script("arguments[0].value = '';", text_height_input)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", text_height_input)
    text_height_input.click()  # Click để kích hoạt ô nhập liệu
    text_height_input.send_keys(Keys.CONTROL, "a")  # Chọn toàn bộ nội dung
    text_height_input.send_keys(Keys.BACKSPACE)  # Xóa nội dung
    text_height_input.send_keys(height)  # Nhập nội dung mới
    print(f"✅ Đã đặt độ dày: {height}mm")
    # Chọn font
    # Tìm phần tử bằng CSS_SELECTOR nếu không có ID
    kerning_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "calcite-input-number[data-test-settings-spacing]"))
    )
    # Cuộn đến phần tử để tránh bị che khuất
    driver.execute_script("arguments[0].scrollIntoView();", kerning_box)
    time.sleep(1)
    # Kiểm tra nếu phần tử có thể nhập liệu
    # Xóa nội dung cũ
    driver.execute_script("arguments[0].value = '';", kerning_box)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", kerning_box)
    kerning_box.click()  # Click để kích hoạt ô nhập liệu
    kerning_box.send_keys(Keys.CONTROL, "a")  # Chọn toàn bộ nội dung
    kerning_box.send_keys(Keys.BACKSPACE)  # Xóa nội dung
    kerning_box.send_keys("0")  # Nhập nội dung mới
    print(f"✅ Đã đặt khoảng cách chữ: 0 mm")

 
    # Tìm phần tử bằng CSS_SELECTOR nếu không có ID
    Line_kerning = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "calcite-input-number[data-test-settings-vspacing]"))
    )
    # Cuộn đến phần tử để tránh bị che khuất
    # Kiểm tra nếu phần tử có thể nhập liệu
    # Xóa nội dung cũ
    driver.execute_script("arguments[0].value = '';", Line_kerning)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", Line_kerning)
    Line_kerning.click()  # Click để kích hoạt ô nhập liệu
    Line_kerning.send_keys(Keys.CONTROL, "a")  # Chọn toàn bộ nội dung
    Line_kerning.send_keys(Keys.BACKSPACE)  # Xóa nội dung
    Line_kerning.send_keys("1.5")  # Nhập nội dung mới
    print(f"✅ Đã đặt khoảng cách dòng: 1.5 mm")
    driver.save_screenshot("debug.png") 

    # Chờ và tìm combobox chứa danh sách font
    font_combobox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "calcite-combobox[selection-mode='single-persist']"))
    )
    driver.execute_script("arguments[0].click();", font_combobox)
    print("✅ Đã mở combobox chọn font")
    # Chờ và chọn một item (ví dụ: "sans-serif")
    # Chờ các option xuất hiện trong DOM
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "calcite-combobox-item"))
    )
    time.sleep(2)  # Chờ combobox load
    # Lấy danh sách tất cả các option
    font_options = driver.find_elements(By.CSS_SELECTOR, "calcite-combobox-item")
    for option in font_options:
        font_name = option.get_attribute("text-label")
        print(f"📌 Tìm thấy font: {font_name}")
        if font_name == "sans-serif":
            driver.execute_script("arguments[0].click();", option)
            break
    else:
        print("⚠️ Không tìm thấy font 'sans-serif'! Hãy kiểm tra lại tên font.")
    # Chờ phần tử xuất hiện trong DOM
    custom_font = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "calcite-switch[data-test-custom-checkbox]"))
    )
    # Cuộn đến phần tử để đảm bảo có thể tương tác
    driver.execute_script("arguments[0].scrollIntoView();", custom_font)
    time.sleep(1)
    # Click bằng JavaScript vì Selenium không hỗ trợ click trực tiếp vào calcite-switch
    driver.execute_script("arguments[0].click();", custom_font)
    # Find the label element and its associated input element to select the font file
    label_element = driver.find_element(
        By.CSS_SELECTOR, "label[data-test-input-label='']"
    )
    file_input_element_id = label_element.get_attribute("for")
    file_input_element = driver.find_element(By.ID, file_input_element_id)
    font_file = os.path.abspath(font)
    file_input_element.send_keys(font_file)
    print(f"✅ Đã chọn font chữ: {font}")

    # Nhấn nút xuất file STL
    export_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "calcite-split-button[data-test-export-stl]"))
    )
    export_button.click()
    print("✅ Đang xuất file STL...")
    # Chờ file tải về và đổi tên file
    time.sleep(5)
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    matching_files = glob.glob(os.path.join(download_folder, "output*.stl"))

    # In danh sách file tìm thấy
    if not matching_files:
        raise FileNotFoundError("⚠️ Không tìm thấy file STL trong thư mục tải xuống.")
    download_path = matching_files[0]  # Lấy file đầu tiên trong danh sách
    new_path = os.path.join(download_folder, "output.stl")
    if os.path.exists(new_path):
        os.remove(new_path)

    os.rename(download_path, new_path)
    print(f"✅ Đã đổi tên file thành: {new_path}")


    # Đóng trình duyệt
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate STL files from text")
    parser.add_argument("names", nargs="+", help="List of names to convert into STL files.")
    args = parser.parse_args()

    # Yêu cầu người dùng nhập name2, width, height, font
    name2 = input("Nhập nội dung thứ hai: ")

    while True:
        try:
            width = float(input("Nhập chiều rộng (mm): "))  # Kiểm tra nhập số hợp lệ
            break
        except ValueError:
            print("⚠️ Vui lòng nhập một số hợp lệ!")

    while True:
        try:
            height = float(input("Nhập chiều cao (mm): "))  # Kiểm tra nhập số hợp lệ
            break
        except ValueError:
            print("⚠️ Vui lòng nhập một số hợp lệ!")

    font = input("Nhập tên font chữ (ví dụ: Arial, Times New Roman, VL_Selfie.otf): ")

    for name in tqdm(args.names, desc="Generating STL files"):
        generate_stl(name.lower(), name2, width, height, font)


