import re

def filter_3_digit_numbers(input_file, output_file):
    """
    Lọc tất cả số có 3 chữ số từ file input và xuất ra file output
    Bao gồm cả số trùng lặp
    """
    try:
        # Đọc nội dung file input
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Tìm tất cả số có đúng 3 chữ số
        # Pattern: \b\d{3}\b - tìm số có đúng 3 chữ số (word boundary)
        three_digit_numbers = re.findall(r'\b\d{3}\b', content)
        
        # Ghi kết quả ra file output
        with open(output_file, 'w', encoding='utf-8') as file:
            for number in three_digit_numbers:
                file.write(number + '\n')
        
        # Thống kê
        print(f"✅ Đã lọc xong!")
        print(f"📁 File input: {input_file}")
        print(f"📁 File output: {output_file}")
        print(f"🔢 Tổng số có 3 chữ số tìm được: {len(three_digit_numbers)}")
        
        # Đếm số unique
        unique_numbers = set(three_digit_numbers)
        print(f"🎯 Số duy nhất: {len(unique_numbers)}")
        print(f"🔄 Số bị trùng lặp: {len(three_digit_numbers) - len(unique_numbers)}")
        
        # Hiển thị một số ví dụ
        print(f"\n📋 Một số ví dụ (10 số đầu tiên):")
        for i, num in enumerate(three_digit_numbers[:10]):
            print(f"  {i+1}. {num}")
        
        if len(three_digit_numbers) > 10:
            print(f"  ... và {len(three_digit_numbers) - 10} số khác")
            
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {input_file}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    # Đường dẫn file
    input_file = "data.txt"
    output_file = "filtered_3_digit_numbers.txt"
    
    # Thực hiện lọc
    filter_3_digit_numbers(input_file, output_file)
