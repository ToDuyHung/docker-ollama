from ollama import AsyncClient, Client
from datetime import datetime

current_date = datetime.now()

formatted_date = current_date.strftime('%d/%m/%Y')


# CÁCH 1:

llm_host = 'http://localhost:13000'
stream_client = Client(host=llm_host)
model = "gemma2:latest"
history = []
invest_source = """{load_document}"""
query = """{load_question}"""
prompt = f"""
Cho đoạn văn bản cung cấp thông tin khuyên nghị của Vietcap như sau
<content>
{invest_source}
</content>

Thông tin trong <content></content> là thông tin về khuyến nghị trong vòng 5 ngày làm việc gần nhất với format được mô tả trong tag <format> dưới đây:
<format>
Tổng quan thị trường - Ngày (DD/MM/YYYY)
    [Chi tiết về thị trường VN30 hoặc VNIndex được liệt kê ở đây ...]
Ngày (DD/MM/YYYY)
    Mã: <3 letters> (examples: ABC, XYZ, ...), Khuyến nghị: "[MUA/BÁN/PHÙ HỢP THỊ TRƯỜNG/KHẢ QUAN/KÉM KHẢ QUAN]", Ngày khuyến nghị gần nhất (DD/MM/YYYY), chi tiết:
            <Các chi tiết...>
            
    Các mã khác trong ngày nếu có...
    
Ngày (Một ngày khác, tối đa 5 ngày gần nhất voi format dd/mm/yyyy)
    Mã: <3 letters> (examples: ABC, XYZ, ...), Khuyến nghị: "[MUA/BÁN/PHÙ HỢP THỊ TRƯỜNG/KHẢ QUAN/KÉM KHẢ QUAN]", Ngày khuyến nghị gần nhất <with datetime format dd/mm/yyyy>, chi tiết:
            <Các chi tiết...>
            
    Các mã khác trong ngày nếu có...
...
</format>

You are a very friendly Customer Service representative of a Securities Joint Stock Company. You should maintain the Customer Service and natural tone during response. Please read the document provided in tag <content></content>, based on the instruction in tag <instruction> </instruction>, answer to the human question .

<instruction>
1. As a friendly Customer Service employee, if a customer simply wants to say hi, greeting or thanks or ask you what information you can help, please friendly response to them shortly. This is impotant for a Customer Service.
2. Không được tự động thêm các thông tin ngoài tài liệu trong <content></content> khi trả lời câu hỏi.
3. Tuyệt đối không nhắc về tài liệu nào trong câu trả lời của mình, hãy xem nó là kiến thức duy nhất của bạn
4. Nhớ rằng suy nghĩ thật kỹ trước khi đưa ra câu trả lời cho user và trả lời một cách ngắn gọn súc tích.
5. Do not need to say hi if customer not say hi, focus on the answer
6. Nếu câu hỏi không đề cập đến một khuyến nghị nào cụ thể, xét tất cả khuyến nghị bao gồm cả Mua/Bán/Phù hợp thị trường/Khả quan/Kém khả quan. Ngược lại nếu khách hàng có đề cập cụ thể đến 1 trong các loại khuyến nghị (Mua/Bán/Phù hợp thị trường/Khả quan/Kém khả quan), hãy tập trung trả lời về loại khuyến nghị đó mà tuyệt đối không đề cập đến các khuyến nghị khác. 
7. if the information in tag <content></content> doesn't allow for a certain response in stock recommendation, provide the exact only answer to the user: "Tôi là bot hỗ trợ các thông tin liên quan đến ý tưởng đầu tư và chưa có đủ thông tin để trả lời câu hỏi này, chúng tôi sẽ cố gắng cập nhật sớm nhất có thể. Bạn có thể tham khảo thêm hai chatbot hỗ trợ chủ đề còn lại. Chúc bạn có một ngày tốt lành!\n"
</instruction>

Biết hôm nay là ngày {formatted_date} and format datetime is DD/MM/YYYY và cố gắng trả lời phù hợp với khoản thời gian khách hàng yêu cầu in Vietnamese

<question>{query}<question>
"""

document="""
Ngày 10/06/2024:
	Mã: GEX, Khuyến nghị "MUA", Ngày khuyến nghị gần nhất 10/06/2024, chi tiết:
		Phân tích Kỹ thuậ:	
			Đang vận động trong kênh xu hướng tăng dần và nằm trong vùng thị trường giá tăng (trên MA200). 
			Tăng với thanh khoản cải thiện vào thứ Sáu tuần trước từ MA10 để tạo đà tăng. 
			Mua GEX với giá mục tiêu ngắn hạn là 25.800 đồng/cổ phiếu và dừng lỗ tại 23.500 đồng/cổ phiếu. 

	Mã: BID, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 10/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Tăng giá mục tiêu cho BID thêm 1,5% lên 55.000 đồng/cổ phiếu và nâng mức khuyến nghị từ PHÙ HỢP THỊ TRƯỜNG lên KHẢ QUAN. 
			Duy trì kỳ vọng NIM sẽ dần cải thiện trong 3 năm tới do chiến lược của ngân hàng nhằm tăng tỷ trọng đóng góp mảng cho vay bán lẻ và do giảm tác động từ các gói hỗ trợ lãi suất cho vay. 
			Tiếp tục giả định BID sẽ phát hành 513 triệu cổ phiếu thông qua phát hành riêng lẻ vào cuối năm 2024 (2,9% cổ phiếu đang lưu hành; giá bán giả định là 50.000 đồng/cổ phiếu) và vào giữa năm 2025 (6,1% cổ phiếu đang lưu hành; giá bán giả định là 55.000 đồng/cổ phiếu). 
			BID đang giao dịch với P/B trượt là 2,5 lần, cao hơn một độ lệch chuẩn so với P/B trượt trung bình 5 năm.

	Mã: GEX, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 10/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Tăng giá mục tiêu cho GEX thêm 12% và nâng khuyến nghị từ PHÙ HỢP THỊ TRƯỜNG lên KHẢ QUAN. 
			Dự báo LNST sau lợi ích CĐTS báo cáo năm 2024 sẽ đạt 853 tỷ đồng (+158% YoY) do chúng tôi kỳ vọng (1) doanh số bán thiết bị điện sẽ phục hồi 16% YoY, và (2) LNTT 950 tỷ đồng từ việc thoái vốn khỏi danh mục năng lượng tái tạo. 
			Dự báo tốc độ tăng trưởng kép (CAGR) LNST giai đoạn 2023-2028 là 41%. 
			GEX có định giá khá hấp dẫn với PE các năm 2024/25 lần lượt ở mức 23.8 lần/31.1 lần, tương ứng PEG là 0,7. 
			GEX đặt kế hoạch trả 1.500 đồng cổ tức tiền mặt (lợi suất 6%) cho năm 2024 nhờ dòng tiền hoạt động mạnh của VGC và GEE. 

	Mã: TV2, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 10/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Vào ngày 7/6/2024, Toyo Group – chủ đầu tư Dự án Sông Hậu 2 (SH2) thông báo rằng họ đã nhận “gói tài trợ mua sắm thiết bị” trị giá lên tới 980 triệu USD từ i-Power Solutions Pte Ltd. Chúng tôi hiểu rằng điều này có nghĩa là Toyo đã đảm bảo được khoảng 1 tỷ USD vốn cho dự án. Mục đích của khoản vốn tài trợ này là để mua các thiết bị cần thiết cho hoạt động EPC (thiết kế, mua sắm, xây dựng) của SH2P. Chúng tôi tin rằng đây là một bước đi tích cực đáng kể hướng tới khả năng SH2P hoàn thành thu xếp vốn vào ngày 30/6, tổng trị giá ước tính là 2,4 tỷ USD. 
			Giá mục tiêu hiện tại của chúng tôi cho TV2 là 58.300 VNĐ/cổ phiếu cho kịch bản có SH2P và 32.000 VNĐ/cổ phiếu cho kịch bản không có SH2P.

	Mã: BSR, Khuyến nghị "MUA", Ngày khuyến nghị gần nhất 10/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Nâng giá mục tiêu cho BSR thêm 41% lên 27.700 đồng/cổ phiếu và nâng khuyến nghị từ PHÙ HỢP THỊ TRƯỜNG lên MUA. 
			Dự báo LNST sau lợi ích CĐTS năm 2024 sẽ giảm 28% YoY xuống 6,1 nghìn tỷ đồng do sản lượng bán giảm 15% YoY do lần bảo dưỡng tổng thể thứ 5 và crack spread thấp hơn so với cùng kỳ. 
			Kỳ vọng triển vọng dài hạn đối với lợi nhuận của BSR sẽ được thúc đẩy bởi dự án nâng cấp & mở rộng, dự kiến đi vào hoạt động từ năm 2028 và giúp tăng sản lượng bán thêm 15%. 
			Định giá hấp dẫn với EV/EBITDA dự phóng năm 2024 ở mức 5 lần, thấp hơn 50% so với P/E trung bình 10 năm của một số công ty cùng ngành trong khu vực. 
			Yếu tố hỗ trợ: Chuyển niêm yết sang HOSE.

Ngày 11/06/2024:
	Mã: SSI, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 11/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Tăng giá mục tiêu đối với SSI thêm 3,8% lên 38.700 đồng/cổ phiếu và nâng khuyến nghị từ PHÙ HỢP THỊ TRƯỜNG lên KHẢ QUAN. 
			Giá mục tiêu cao hơn của chúng tôi chủ yếu do tác động tích cực từ việc cập nhật giá mục tiêu sang giữa năm 2025 trong khi dự báo tổng LNST sau lợi ích CĐTS giai đoạn 2024-2028 của chúng tôi gần như không đổi so với dự báo trước. 
			Tăng dự báo doanh thu mảng cho vay ký quỹ do (1) chúng tôi tăng dự báo giá trị giao dịch trung bình hàng ngày (GTGDTB) thêm 5,4% trong giai đoạn 2024-2025 và (2) chúng tôi tăng dự báo dư nợ cho vay ký quỹ trên mỗi tài khoản khách hàng. 
			Điều chỉnh giảm 3,2% dự báo LNST sau lợi ích CĐTS năm 2024 xuống còn 3 nghìn tỷ đồng (+29,6% YoY) do giảm 3.8% doanh thu dự phóng mảng môi giới trong năm 2024. Mức giảm này là do chúng tôi giảm 30 điểm cơ bản đối với dự báo thị phần mảng môi giới của SSI xuống 9,5%. 

	Mã: BWE, Khuyến nghị "PHÙ HỢP THỊ TRƯỜNG", Ngày khuyến nghị gần nhất 11/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Sản lượng nước thương phẩm trong tháng 5 đạt 17,3 triệu m3 (+12% YoY), nâng tổng sản lượng 5T 2024 đạt 82,1 triệu m3 (+9,6% YoY), hoàn thành 43% dự báo cả năm của chúng tôi, cao hơn đáng kể so với dự kiến. 
			Doanh thu và LNST công ty mẹ sơ bộ 5T 2024 lần lượt đạt 1.493 tỷ đồng (+8% YoY; 39% dự báo năm 2024 của chúng tôi) và 270 tỷ đồng (-8% YoY). 
			Chúng tôi ước tính LNST sau lợi ích CĐTS hợp nhất là 284 tỷ đồng (-8% YoY) và hoàn thành 38% dự báo cả năm của chúng tôi. 
			Chúng tôi hiện đưa ra giá mục tiêu là 44.700 đồng/cổ phiếu cho BWE. 

Ngày 12/06/2024:
	Mã: POW, Khuyến nghị "PHÙ HỢP THỊ TRƯỜNG", Ngày khuyến nghị gần nhất 12/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Công bố sản lượng điện thương phẩm tăng 11% YoY trong tháng 5, chủ yếu do sản lượng điện thương phẩm của nhà máy Vũng Áng tăng mạnh (+76% YoY). 
			Giá trên thị trường phát điện cạnh tranh (CGM) của ngành  giảm 8% MoM xuống 1.600 đồng/kWh trong tháng 5.  
			Sản lượng điện thương phẩm 5 tháng đầu năm 2024 đạt 7 tỷ kWh (+1% YoY) với doanh thu đạt 12,7 nghìn tỷ đồng (-5% YoY), lần lượt hoàn thành 42% và 39% dự báo cả năm của chúng tôi.  
			POW đã giải quyết tranh chấp thuê đất của công ty với CTCP Tín Nghĩa bằng việc ký hợp đồng thuê 30,8 ha đất vào ngày 27/05/2024, và được Bộ Tài nguyên và Môi trường cấp giấy chứng nhận quyền sử dụng đất. 
			Chúng tôi hiện đưa ra giá mục tiêu là 13.200 đồng/cổ phiếu cho POW. 

	Mã: PVS, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 12/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Chốt mức cổ tức tiền mặt năm 2023 là 700 đồng/cổ phiếu, phù hợp với dự báo của chúng tôi. 
			Dự kiến sẽ chia cổ tức tiền mặt năm 2024 ở mức 700 đồng/cổ phiếu, phù hợp với dự báo của chúng tôi. 
			Công ty cần vốn đầu tư XDCB lớn, lên đến 70,6 nghìn tỷ đồng và nhu cầu đầu tư bằng vốn chủ sở hữu ở mức 17,7 nghìn tỷ đồng trong giai đoạn 2024-2030 để nâng cao năng lực nhà thầu và đầu tư vào các dự án mới. 
			PVS cần thêm 8,9 nghìn tỷ đồng vốn chủ sở hữu. Để đáp ứng nhu cầu này, PVS có thể tăng vốn cổ phần của công ty thêm 8,9 nghìn tỷ đồng thông qua việc phát hành cổ phiếu mới và chia cổ tức cổ phiếu. 
			Chúng tôi hiện đưa ra giá mục tiêu là 50.400 đồng/cổ phiếu cho PVS. 

	Mã: VEA, Khuyến nghị "PHÙ HỢP THỊ TRƯỜNG", Ngày khuyến nghị gần nhất 12/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Dựa theo dữ liệu từ Hiệp hội các nhà sản xuất ô tô Việt Nam (VAMA) và Hyundai Thành Công, chúng tôi ước tính doanh số bán lẻ xe ô tô tăng 29% YoY trong tháng 5/2024.  
			Trong 5 tháng đầu năm 2024, doanh số bán lẻ xe ô tô giảm 9% YoY. Tuy nhiên, do Chính phủ có kế hoạch thực hiện chính sách cắt giảm phí đăng ký trước bạ trong nửa cuối năm 2024, chúng tôi nhận thấy không có rủi ro đối với dự báo hiện tại của chúng tôi. 
			Chúng tôi hiện có giá mục tiêu là 40.500 đồng/cổ phiếu cho VEA 

	Mã: VIB, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 12/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Theo ban lãnh đạo, phương án giảm FOL xuống 4,99% phù hợp với quy định của luật hiện hành.  
			Về lộ trình thoái vốn của CBA, ban lãnh đạo cho biết VIB chỉ mới biết đến mục tiêu của CBA sau khi Ngân hàng Nhà nước (NHNN) trả lại văn bản chấp thuận thoái vốn. Hiện tại, VIB chưa có thông tin chi tiết về kế hoạch thoái vốn cụ thể sắp tới của CBA. 
			Về kế hoạch tìm kiếm đối tác chiến lược mới của VIB, ban lãnh đạo cho biết ngân hàng hiện chưa thực hiện quá trình này vì tỷ lệ sở hữu nước ngoài còn lại là 9,5%. 
			Tổng quan về CBA: FOL hiện tại của VIB là 20,499%, trong đó cổ đông lớn CBA sở hữu tỷ lệ 19.854. Vào năm 2019, CBA đã rút khỏi HĐQT của VIB.  
			Chúng tôi cho rằng việc giảm trần FOL xuống 4,99% sẽ cho phép VIB (1) chủ động trong việc lựa chọn đối tác chiến lược tiềm năng và (2) tận dụng tỷ lệ sở hữu của nhà đầu tư nước ngoài nếu ngân hàng có kế hoạch huy động vốn trong tương lai. 
			Chúng tôi hiện có giá mục tiêu là 26.000 đồng/cổ phiếu cho VIB. 

	Mã: PPC, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 12/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Thông qua kế hoạch lạc quan cho năm 2024 với doanh thu 8,8 nghìn tỷ đồng (+51% YoY) và LNTT là 427 tỷ đồng (+12% YoY). 
			Thông qua phương án cổ tức bằng tiền mặt năm 2023 là 2.775 đồng/cổ phiếu. 
			Dự kiến trả cổ tức năm 2024 với tỷ lệ 6% mệnh giá (chưa xác định tiền mặt hay cổ phiếu).
			Ban lãnh đạo công bố lợi nhuận sơ bộ 5 tháng đầu năm 2024 (5T 2024) từ mảng sản xuất điện là 135 tỷ đồng (31% dự báo cả năm của chúng tôi), thấp hơn một chút so với kỳ vọng của chúng tôi  
			Chúng tôi hiện có giá mục tiêu là 16.700 đồng/cổ phiếu cho PPC. 

Ngày 13/06/2024:
	Mã: PNJ, Khuyến nghị "MUA", Ngày khuyến nghị gần nhất 13/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Đang vận động trong biên độ từ 91.500 đến 104.000 đồng/cp kể từ đầu tháng 3. 
			Tăng với thanh khoản cao ngày hôm qua, đóng cửa ở mức cao nhất trong 3 tuần và trên MA50 tại 96.000 đồng/cp. 
			Mua PNJ với giá mục tiêu ngắn hạn là 103.500 đồng/cp và dừng lỗ tại 96.000 đồng/cp. 
			
	Mã: CTR, Khuyến nghị "PHÙ HỢP THỊ TRƯỜNG", Ngày khuyến nghị gần nhất 13/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Công bố kết quả sơ bộ 5T 2024 với doanh thu đạt 4,6 nghìn tỷ đồng (+10% YoY) và LNTT đạt 250 tỷ đồng (+5% YoY), thấp hơn một chút so với kỳ vọng của chúng tôi. 
			Chúng tôi hiện đưa giá mục tiêu là 138.000 đồng/cổ phiếu cho CTR nhưng nhận thấy rủi ro điều chỉnh giảm nhẹ đối với dự báo năm 2024 của chúng tôi. 

	Mã: VHC, Khuyến nghị "PHÙ HỢP THỊ TRƯỜNG", Ngày khuyến nghị gần nhất 13/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Công bố KQKD 5T 2024 với doanh thu tăng 24% YoY đạt 5 nghìn tỷ đồng, chủ yếu nhờ doanh số bán phi lê cá tra đông lạnh và các sản phẩm liên quan tăng 23% YoY, phù hợp với dự báo hiện tại của chúng tôi. 
			Trong 5T 2024, doanh thu của VHC duy trì mức tăng trưởng dương trên các thị trường trọng điểm, bao gồm Mỹ (+9% YoY), Châu Âu (+18% YoY) và Trung Quốc (+16% YoY). 
			Chúng tôi đưa ra giá mục tiêu là 80.200 đồng/cổ phiếu cho VHC 

	Mã: DCM, Khuyến nghị "PHÙ HỢP THỊ TRƯỜNG", Ngày khuyến nghị gần nhất 13/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Ban lãnh đạo lạc quan về mức thuế GTGT 5% đối với phân bón sẽ được phê duyệt vào cuối năm 2024, sản lượng NPK tăng mạnh trong nửa cuối năm và hiệu suất hoạt động cao ở mức 115% sẽ được duy trì trong những năm tới. 
			Thông qua phương án chia cổ tức bằng tiền mặt 2.000 đồng/cổ phiếu cho năm 2023. Ngày đăng ký cuối cùng: 25/6/2024. Ngày thanh toán: 11/7/2024. 
			Thông qua mức cổ tức thận trọng bằng tiền mặt là 1.000 đồng/cổ phiếu cho năm 2024. 
			Kế hoạch thận trọng cho năm 2024 với doanh thu 11,9 nghìn tỷ đồng và LNST 795 tỷ đồng. 
			Chúng tôi hiện đưa ra giá mục tiêu là 36.000 đồng/cổ phiếu cho DCM 

	Mã: TV2, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 13/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Ngày 12/06/2024, Tập đoàn Toyo – chủ đầu tư của dự án Sông Hậu 2 (SH2P) – công bố rằng công ty đã ký kết thỏa thuận đấu nối lưới điện với Tổng công ty Truyền tải điện Quốc gia (EVNNPT) về việc đấu nối lưới điện vào hệ thống điện Quốc gia thông qua trạm biến áp 500kV của Khu phức hợp Điện lực Sông Hậu. 
			Chúng tôi cho rằng diễn biến này là một cột mốc tích cực trong công tác chuẩn bị cho SH2P, nhấn mạnh khả năng cao dự án sẽ sớm khởi công và phát điện trong tương lai. 
			Chúng tôi hiện đưa ra giá mục tiêu cho TV2 là 58.300 đồng/cổ phiếu nếu có SH2P và 32.000 đồng/cổ phiếu không có SH2P. 

	Mã: BWE, Khuyến nghị "PHÙ HỢP THỊ TRƯỜNG", Ngày khuyến nghị gần nhất 13/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Ông Nguyễn Thanh Phong, Thành viên HĐQT BWE, thông báo sẽ mua thêm 1 triệu cổ phiếu, nâng tỷ lệ sở hữu tại công ty từ 0,9% lên 1,36% (tổng cộng 3 triệu cổ phiếu). 
			Việc mua bán sẽ được thực hiện thông qua đấu giá hoặc thỏa thuận, dự kiến diễn ra trong khoảng thời gian từ ngày 13/6/2024 đến ngày 12/7/2024. 
			Chúng tôi hiện đưa ra giá mục tiêu là 44.700 đồng/cổ phiếu cho BWE.

Ngày 14/06/2024:
	Mã: BVB, Khuyến nghị "MUA", Ngày khuyến nghị gần nhất 14/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Đang vận động trong kênh tăng giá kể từ khi vượt qua MA50 vào đầu tháng 5. 
			Tăng với thanh khoản mạnh ngày hôm qua và đóng cửa trên đường MA10, để khởi tạo đà tăng ngắn hạn. 
			Mua BVB với giá mục tiêu ngắn hạn 15.000 đồng/cổ phiếu và dừng lỗ tại 12.300 đồng/cổ phiếu.
			
Ngày 17/06/2024:
	Mã: PVS, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 17/06/2024, chi tiết:
		Phân tích Cơ bản:	
			PVS kỳ vọng sẽ có bước đột phá đáng kể về doanh thu và lợi nhuận vào năm 2025, được thúc đẩy bởi lượng công việc M&C đáng kể. 
			Về dự án Lô B Ô Môn, PVS kỳ vọng không có sự chậm trễ đáng kể trong Quyết định Đầu tư Cuối cùng (FID) của Tập đoàn Dầu khí Việt Nam và nhấn mạnh công việc tiếp tục với tư cách là nhà thầu, với các khoản giải ngân kịp thời và thanh toán đầy đủ từ các nhà điều hành. 
			Báo cáo KQKD sơ bộ 5T 2024 với doanh thu hợp nhất đạt 6,8 nghìn tỷ đồng (+11% YoY) và LNTT hợp nhất đạt 573 tỷ đồng (+50% YoY), tương đương với 24% và 34% dự báo cả năm của chúng tôi. 
			Vốn đầu tư XDCB cho giai đoạn 2024-2030 là 70,6 nghìn tỷ đồng, với yêu cầu vốn chủ sở hữu là 17,6 nghìn tỷ đồng. Để đáp ứng yêu cầu này, PVS có thể tăng vốn cổ phần thêm 8,9 nghìn tỷ đồng bằng cách phát hành cổ phiếu mới và trả cổ tức bằng cổ phiếu. Tuy nhiên, kế hoạch này vẫn đang trong giai đoạn đầu. 
			Chúng tôi hiện đưa ra giá mục tiêu là 50.400 đồng/cổ phiếu cho PVS.

	Mã: TV2, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 17/06/2024, chi tiết:
		Phân tích Cơ bản:	
			Đưa ra kế hoạch thận trọng cho năm 2024, không bao gồm dự án Sông Hậu 2 (SH2P) với doanh thu 1.272 tỷ đồng (+20% YoY) và LNTT là 66 tỷ đồng (đi ngang YoY). 
			Doanh thu sơ bộ nửa đầu năm 2024 đạt 400 tỷ đồng (31% kế hoạch năm 2024), hoàn thành 26% dự báo cả năm của chúng tôi nếu không có SH2P. 
			Thông qua phương án chia cổ tức bằng tiền mặt năm 2023 & 2024 với tỷ lệ 10% mệnh giá (1.000 đồng/cổ phiếu), phù hợp với kỳ vọng của chúng tôi. 
			Theo Chủ tịch TV2, để đáp ứng thời hạn thu xếp tài chính trước ngày 30/6/2024, SH2P cần nhận được (1) thỏa thuận tài trợ vốn (điều khoản & điều kiện tài chính), (2) thư chấp nhận tài trợ tài chính của bên cho vay và (3) khoản giải ngân đầu tiên (FDP). Ông chia sẻ, 2 tiêu chí đầu đã đạt và chờ tiêu chí cuối cùng. 
			Chúng tôi hiện đưa ra giá mục tiêu là 58.300 đồng/cổ phiếu cho TV2 nếu có SH2P và 32.000 đồng/cổ phiếu nếu không có SH2P.

Ngày 18/06/2024:
	Mã: MBB, Khuyến nghị "MUA", Ngày khuyến nghị gần nhất 18/06/2024, chi tiết:
		Phân tích Cơ bản:
			HĐQT nhiệm kỳ 2024-2029 (11 thành viên trong đó có 7 thành viên mới); BKS nhiệm kỳ 2024-2029 (5 thành viên trong đó có 2 thành viên mới). Tất cả các thành viên HĐQT, BKS mới đều đã có nhiều năm kinh nghiệm làm việc tại MBB, Tập đoàn Vietel và các cổ đông lớn khác của MBB. 
			Kỳ vọng hiện tại của ban lãnh đạo về KQKD 6 tháng đầu năm 2024: LNTT hợp nhất đạt hơn 13 nghìn tỷ đồng (+5% YoY), tăng trưởng tín dụng 5-6% (so với ước tính tăng trưởng tín dụng toàn hệ thống ở mức 4%-5%); tỷ lệ nợ xấu < 2% (so với tỷ lệ nợ xấu quý 1/2024 là 2,5%). 
			Chúng tôi hiện đưa ra giá mục tiêu là 30.000 đồng/cổ phiếu cho MBB.

	Mã: GVR, Khuyến nghị "PHÙ HỢP THỊ TRƯỜNG", Ngày khuyến nghị gần nhất 18/06/2024, chi tiết:
		Phân tích Cơ bản:
			Thông qua kế hoạch LNTT các năm 2024/25 lần lượt là 4,1 nghìn tỷ đồng (đi ngang YoY) và 5,1 nghìn tỷ đồng (+23% YoY), tương đương với 85% và 84% dự báo tương ứng của chúng tôi. 
			Thông qua mức cổ tức năm 2023 là 3% mệnh giá, hiện chưa được chi trả. 
			Thông qua mức cổ tức năm 2024 là 3% mệnh giá. GVR trước đây luôn trả cổ tức bằng tiền mặt. 
			Thông qua việc bổ nhiệm ông Đỗ Hữu Phước làm thành viên HĐQT và ông Nguyễn Đông Phong làm thành viên HĐQT độc lập. 
			Chúng tôi hiện đưa ra giá mục tiêu là 29.900 đồng/cổ phiếu cho GVR. 

Ngày 19/06/2024:
	Mã: BMP, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 19/06/2024, chi tiết:
		Phân tích Cơ bản:
			Duy trì khuyến nghị KHẢ QUAN cho BMP mặc dù điều chỉnh giảm 8% giá mục tiêu xuống còn 109.700 đồng/cổ phiếu. 
			Điều chỉnh giảm 9% mỗi năm cho dự báo LNST sau lợi ích CĐTS các năm 2024/25/26 do giả định sản lượng bán hàng thấp hơn và chi phí bán hàng & quản lý (SG&A)/doanh thu tăng. 
			Điều chỉnh giảm giả định cổ tức bằng tiền mặt năm 2024 xuống 10.800 đồng/cổ phiếu (so với 11.500 đồng/cổ phiếu trong dự báo trước đây), 
			Định giá hấp dẫn với P/E trung bình dự phóng giai đoạn 2024-25 là 9,9 lần. Giá mục tiêu của chúng tôi tương ứng P/E trung bình giai đoạn 2024-25 của BMP là 10,1 lần, thấp hơn P/E trung bình 5 năm/10 năm lần lượt là 10,9 lần/11,1 lần. 
	
	Mã: FPT, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 19/06/2024, chi tiết:
		Phân tích Cơ bản:
			Công bố KQKD 5T 2024 với doanh thu đạt 23,9 nghìn tỷ đồng (+20% YoY) và LNST sau lợi ích CĐTS đạt 3,1 nghìn tỷ đồng (+21% YoY), nhìn chung phù hợp với quan điểm của chúng tôi về tăng trưởng lợi nhuận mạnh của FPT trong năm 2024. 
			Dịch vụ CNTT toàn cầu: Doanh thu +30% YoY & LNTT +25% YoY. Nhật Bản và APAC dẫn đầu với tăng trưởng doanh thu lần lượt đạt 34% YoY và 31% YoY. 
			Chúng tôi hiện đưa ra giá mục tiêu là 147.900 đồng/cổ phiếu cho FPT. 

	Mã: NLG, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 19/06/2024, chi tiết:
		Phân tích Cơ bản:
			Công bố công ty đã hoàn tất chuyển nhượng 25% cổ phần tại dự án Paragon (Đồng Nai; 45 ha) cho đối tác Nhật Bản vào tháng 6/2024. 
			Giao dịch này dự kiến mang lại 662 tỷ đồng doanh thu và khoảng 200 tỷ đồng LNST sau lợi ích CĐTS, và sẽ được ghi nhận vào quý 2/2024. 
			Dự án Paragon (tổng cộng khoảng 520 căn thấp tầng; NLG sở hữu 50% cổ phần) đã hoàn thành đầy đủ công tác đền bù giải phóng mặt bằng và cấp giấy chứng nhận quyền sử dụng đất cho toàn bộ dự án. 
			Chúng tôi hiện đưa ra giá mục tiêu là 48.700 đồng/cổ phiếu cho NLG. 

	Mã: ACG, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 19/06/2024, chi tiết:
		Phân tích Cơ bản:
			Công bố trả cổ tức tiền mặt còn lại của năm 2023 ở mức 800 đồng/cổ phiếu. Ngày giao dịch không hưởng quyền là 24/06/2024 và ngày thanh toán dự kiến là 10/07/2024. 
			Đối với năm 2024, ĐHCĐ đã thông qua mức cổ tức tối thiểu 15% trên mệnh giá, bằng tiền mặt hoặc bằng cổ phiếu. Công ty sẽ phấn đấu nâng tỷ lệ này lên 20%-25% nếu KQKD năm 2024 thuận lợi. 
			Chúng tôi hiện đưa ra giá mục tiêu là 43.100 đồng/cổ phiếu cho ACG. 

Ngày 20/06/2024:
	Mã: VPB, Khuyến nghị "MUA", Ngày khuyến nghị gần nhất 20/06/2024, chi tiết:
		Phân tích Cơ bản:
		Tăng mạnh với thanh khoản cao ngày hôm qua từ ngưỡng hỗ trợ MA10 và MA50 tại vùng 18.500-18.700 đồng/cổ phiếu, vượt trội hơn so với VN-Index. 
		Mua VPB với giá mục tiêu ngắn hạn 21.000 đồng/cổ phiếu và dừng lỗ tại 18.500 đồng/cổ phiếu.

	Mã: KBC, Khuyến nghị "MUA", Ngày khuyến nghị gần nhất 20/06/2024, chi tiết:
		Phân tích Cơ bản:
			Thông qua việc duy trì kế hoạch năm 2024 đối với tổng thu nhập (bao gồm doanh thu, thu nhập tài chính, và các thu nhập khác) là 9 nghìn tỷ đồng (+48% YoY)và LNST là 4 nghìn tỷ đồng (+78% YoY). 
			Thông qua kế hoạch phát hành riêng lẻ tối đa 250 triệu cổ phiếu (33% cổ phiếu đang lưu hành) cho không quá 100 nhà đầu tư, dự kiến thực hiện trong giai đoạn 2024-2025. 
			KBC dự kiến sử dụng số tiền thu được để bổ sung/mở rộng vốn lưu động, tái cơ cấu nợ vay, đầu tư vào các công ty con/công ty liên doanh/công ty liên kết, và tiến hành các hoạt động M&A. 
			Chúng tôi hiện đưa ra giá mục tiêu là 39.400 đồng/cổ phiếu cho KBC.

	Mã: GEX, Khuyến nghị "KHẢ QUAN", Ngày khuyến nghị gần nhất 20/06/2024, chi tiết:
		Phân tích Cơ bản:
			Công ty TNHH Sembcorp Solar Vietnam, công ty con do Sembcorp sở hữu 100%, công bố đã hoàn tất thương vụ mua lại danh mục năng lượng tái tạo với công suất 196 MW từ GEX. 
			Ngoài ra, Sembcorp có kế hoạch mua lại tài sản thủy điện 49 MW tại nhà máy thủy điện Sông Bung, theo đó GEX sẽ hoàn tất thoái 73% tỷ lệ sở hữu, khi nhận được các phê duyệt theo quy định vào nửa cuối năm 2024. 
			Chúng tôi ước tính tổng số tiền thu được từ việc thoái vốn là 950 tỷ đồng mà GEX kỳ vọng sẽ ghi nhận trong KQKD quý 2. 
			Chúng tôi hiện đưa ra giá mục tiêu là 26.200 đồng/cổ phiếu cho GEX.

Tổng quan thị trường - Ngày 20/06/2024
	Hỗ trợ MA20 tại 1.303 điểm đã giúp VN30 hồi phục lại về phía cuối ngày và đóng cửa tăng nhẹ. Chỉ số có thể sẽ kiểm định kháng cự MA10 tại 1.317 điểm trong nỗ lực khôi phục lại đà tăng ngắn hạn.
"""

def generate_prompt(question, prompt_template: str, **kwargs):
    docs = document
    prompt_template = prompt_template.replace("{load_document}", docs).replace("{load_question}", question)
    return prompt_template

question="Ngày 20/06/2024 thị trường như thế nào"
prompt_question =  generate_prompt(question, prompt)
# print(prompt_question)


messages = [{
            "role": "system",
            'content': "You are a friendly Customer Service representative of Vietcap Securities Joint Stock Company. You should maintain the Customer Service and natural tone during response and answer everyting in Vietnamese.",
        },] + history + [{
            "role": "user",
            "content" : prompt_question
        }]
# for i in stream_client.chat(model=model, messages=messages, stream=True):
    # print(i["message"]["content"], end="", flush=True)
    
#  ========================================= CÁCH 2: ===================================================
import time
import ollama
s = time.time()
stream = ollama.chat(
    model='gemma2', # 'lamma3', 'llama3.1'
    messages=messages,
    stream=True,
)

for i in stream:
  print(i["message"]["content"], end="", flush=True)
print(time.time() - s)
