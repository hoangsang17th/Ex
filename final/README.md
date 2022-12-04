## Chatbot phân loại ý định

```=> Một ứng dụng học theo vòng lặp được giám sát```

Một bộ phân loại ý định được sử dụng để khớp đầu ra của quy trình NLU với các nhãn được xác định trước có liên quan trong tập dữ liệu huấn luyện. Ví dụ: khi người dùng nói với chatbot: “Tôi muốn đặt một chuyến bay từ Houston đến LA”, bộ phân loại ý định sẽ phân loại ngữ cảnh và chuỗi từ dưới nhãn “đặt chuyến bay”.

### Thử thách
`Mục tiêu của Chatbots là tạo ra các cuộc trò chuyện toàn diện giống như con người để đáp ứng mong đợi của người dùng. Tuy nhiên, chatbot gặp phải những hạn chế trong việc hiểu ý định của người dùng vì:`

+ Ngôn ngữ tự nhiên là khó khăn , ngay cả đối với con người.
+ Là con người, chúng ta có khả năng thể hiện ý định của mình bằng cách sử dụng các cấu trúc ngôn ngữ khác nhau.
+ Người dùng đôi khi mắc lỗi chính tả và sử dụng từ khóa thay vì câu hoàn chỉnh.
+ Hầu hết các phản hồi của chatbot được giới hạn ở các ý định được xác định trước trong bộ dữ liệu được đào tạo.

### Khắc phục
`Tuy nhiên, một số hạn chế có thể được giải quyết bằng cách tích hợp các giải pháp khác nhau:`


+ Người dùng có thể tạo ý định tùy chỉnh. Ví dụ: trong Amazon Alexa, người dùng có thể đặt quy tắc để chatbot thực hiện một tác vụ cụ thể bằng cách cung cấp tên và danh sách các cách nói mà người dùng sẽ nói để gọi ý định này.
+ Việc tăng khối lượng dữ liệu đào tạo sẽ làm giảm biên độ lỗi trong phát hiện ý định.


[x] Chuẩn bị dữ liệu
[x] Nghiên cứu thuật toán
[x] Viết code hoặc sử dụng thư viện
[x] Training dữ liệu
[x] Chạy mô hình
[x] Điều chỉnh các tham số của mô hình và dữ liệu đầu vào để nhận được chất lượng tốt hơn
[x] Cần đánh giá chất lượng của mô hình thông qua các phương pháp đánh giá tương ứng, có thể so sánh qua nhiều phương pháp đánh giá khác nhau
[] Nên so sánh giữa các thuật toán cho cùng 1 đề tài
[x] Nên triển khai ứng dụng trên giao diện người dùng (trên web, app...)

Retrieval-based Chatbots