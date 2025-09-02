#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def analyze_winning_numbers():
    """
    Phân tích file a.txt để tìm 2 số có khả năng thắng cao nhất
    Dựa trên luật: "Người chiến thắng sẽ là người có con số gần nhất"
    """
    
    # Đọc tất cả các số từ file
    with open('a.txt', 'r', encoding='utf-8') as file:
        numbers = []
        for line in file:
            line = line.strip()
            if line and line.isdigit():
                numbers.append(int(line))
    
    # Sắp xếp các số theo thứ tự tăng dần
    numbers.sort()
    
    print(f"Tổng số lượng số đã chọn: {len(numbers)}")
    print(f"Số nhỏ nhất: {min(numbers):03d}")
    print(f"Số lớn nhất: {max(numbers):03d}")
    print(f"Khoảng số: {min(numbers):03d} - {max(numbers):03d}")
    
    # Tìm các khoảng trống lớn nhất giữa các số liên tiếp
    gaps = []
    for i in range(len(numbers) - 1):
        gap_size = numbers[i + 1] - numbers[i]
        if gap_size > 1:  # Chỉ quan tâm đến khoảng trống > 1
            gap_start = numbers[i]
            gap_end = numbers[i + 1]
            middle_point = (gap_start + gap_end) / 2
            gaps.append({
                'start': gap_start,
                'end': gap_end,
                'size': gap_size,
                'middle': middle_point
            })
    
    # Sắp xếp các khoảng trống theo kích thước giảm dần
    gaps.sort(key=lambda x: x['size'], reverse=True)
    
    print("\n=== 10 KHOẢNG TRỐNG LỚN NHẤT ===")
    for i, gap in enumerate(gaps[:10]):
        print(f"{i+1:2d}. Khoảng {gap['start']:03d} - {gap['end']:03d} "
              f"(kích thước: {gap['size']:2d}, điểm giữa: {gap['middle']:.1f})")
    
    # Chọn 2 số tối ưu từ khoảng trống lớn nhất
    best_recommendations = []
    
    for gap in gaps[:5]:  # Xem xét 5 khoảng trống lớn nhất
        gap_start = gap['start']
        gap_end = gap['end']
        gap_size = gap['size']
        
        if gap_size >= 3:  # Chỉ chọn từ khoảng trống đủ lớn
            # Chọn 2 số ở vị trí 1/3 và 2/3 của khoảng trống
            pos1 = gap_start + gap_size // 3
            pos2 = gap_start + (gap_size * 2) // 3
            
            # Đảm bảo không trùng với số đã có
            while pos1 in numbers:
                pos1 += 1
            while pos2 in numbers:
                pos2 += 1
                
            # Đảm bảo vẫn trong khoảng trống
            if pos1 < gap_end and pos2 < gap_end and pos1 != pos2:
                distance_to_nearest1 = min(abs(pos1 - gap_start), abs(pos1 - gap_end))
                distance_to_nearest2 = min(abs(pos2 - gap_start), abs(pos2 - gap_end))
                
                best_recommendations.append({
                    'numbers': [pos1, pos2],
                    'gap_info': gap,
                    'distances': [distance_to_nearest1, distance_to_nearest2],
                    'min_distance': min(distance_to_nearest1, distance_to_nearest2)
                })
    
    # Sắp xếp theo khoảng cách tối thiểu đến số gần nhất (càng lớn càng tốt)
    best_recommendations.sort(key=lambda x: x['min_distance'], reverse=True)
    
    print("\n=== PHÂN TÍCH CHI TIẾT ===")
    
    # Tìm các số xuất hiện nhiều lần (có lợi thế về thời gian comment)
    from collections import Counter
    number_counts = Counter(numbers)
    duplicates = {num: count for num, count in number_counts.items() if count > 1}
    
    if duplicates:
        print(f"\nCác số xuất hiện nhiều lần:")
        for num, count in sorted(duplicates.items()):
            print(f"  {num:03d}: {count} lần")
    
    print(f"\n=== GỢI Ý 2 SỐ TỐI ÙU ===")
    
    if best_recommendations:
        best = best_recommendations[0]
        num1, num2 = best['numbers']
        gap = best['gap_info']
        
        print(f"\nSố đề xuất 1: {num1:03d}")
        print(f"Số đề xuất 2: {num2:03d}")
        print(f"\nLý do chọn:")
        print(f"- Nằm trong khoảng trống lớn: {gap['start']:03d} - {gap['end']:03d} (kích thước {gap['size']})")
        print(f"- Khoảng cách đến số gần nhất: {best['distances'][0]} và {best['distances'][1]}")
        print(f"- Khả năng thắng cao vì ít số cạnh tranh trong vùng này")
        
        # Tính xác suất thắng ước tính
        total_unused_range = 999 - len(set(numbers))
        win_probability = (best['min_distance'] * 2) / total_unused_range * 100
        print(f"- Ước tính xác suất thắng: ~{win_probability:.1f}%")
        
    else:
        # Fallback: chọn từ các vùng ít số nhất
        print("Không tìm thấy khoảng trống lớn phù hợp. Đề xuất dựa trên phân tích khác:")
        
        # Chia thành các khoảng và tìm khoảng ít số nhất
        ranges = {
            "000-099": [n for n in numbers if 0 <= n <= 99],
            "100-199": [n for n in numbers if 100 <= n <= 199],
            "200-299": [n for n in numbers if 200 <= n <= 299],
            "300-399": [n for n in numbers if 300 <= n <= 399],
            "400-499": [n for n in numbers if 400 <= n <= 499],
            "500-599": [n for n in numbers if 500 <= n <= 599],
            "600-699": [n for n in numbers if 600 <= n <= 699],
            "700-799": [n for n in numbers if 700 <= n <= 799],
            "800-899": [n for n in numbers if 800 <= n <= 899],
            "900-999": [n for n in numbers if 900 <= n <= 999]
        }
        
        print("\nPhân bố theo khoảng:")
        for range_name, range_numbers in ranges.items():
            print(f"  {range_name}: {len(range_numbers)} số")
        
        # Tìm khoảng ít số nhất
        min_range = min(ranges.items(), key=lambda x: len(x[1]))
        print(f"\nKhoảng ít số nhất: {min_range[0]} ({len(min_range[1])} số)")
        
        # Đề xuất 2 số từ khoảng này
        range_start = int(min_range[0].split('-')[0])
        range_end = int(min_range[0].split('-')[1])
        used_in_range = set(min_range[1])
        
        suggestions = []
        for num in range(range_start, range_end + 1):
            if num not in used_in_range:
                suggestions.append(num)
            if len(suggestions) >= 2:
                break
        
        if len(suggestions) >= 2:
            print(f"\nĐề xuất: {suggestions[0]:03d} và {suggestions[1]:03d}")
            print(f"Lý do: Khoảng {min_range[0]} có ít số cạnh tranh nhất")

if __name__ == "__main__":
    analyze_winning_numbers()
