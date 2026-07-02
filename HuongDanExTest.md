Dưới đây là phần 1 của bản chuyển thể Markdown từ tài liệu bạn đã tải lên (Bao gồm Mục lục và các mục từ 1.0 đến 1.3).

HƯỚNG DẪN GÓI LỆNH ex-test v3.1 

**Tác giả:** Trần Anh Tuấn 

**Phát triển:** Dương Phước Sang 

---

Mục lục 

* 
**1 Cấu trúc và lệnh gõ các loại câu hỏi thông dụng** 


* 1.0 Thiết lập lưu đáp án, lưu lời giải chi tiết 


* 1.1 Câu trắc nghiệm chọn 1 trong nhiều phương án lựa chọn 


* 1.1.1 Các tuỳ chọn của `choice` 


* 1.1.2 Một số tuỳ chỉnh 


* 1.1.3 Gõ câu trắc nghiệm với đặc trưng riêng của môn tiếng Anh 




* 1.2 Câu trắc nghiệm được chọn 1 hoặc nhiều hơn 1 phương án 


* 1.3 Câu trắc nghiệm Đúng/Sai 


* 1.3.1 Các tuỳ chọn của `\choiceTF` 


* 1.3.2 Đồng bộ tuỳ chọn cho `choiceTF` toàn tài liệu 


* 1.3.3 Một số tuỳ chỉnh 




* 1.4 Câu trắc nghiệm trả lời ngắn 


* 1.4.1 Các tuỳ chọn của `shortans` 


* 1.4.2 Đồng bộ tuỳ chọn cho `shortans` toàn tài liệu 


* 1.4.3 Một số tuỳ chỉnh 


* 1.4.4 Câu hỏi có nhiều ý nhỏ trả lời ngắn bằng `shortans` 




* 1.5 Câu trắc nghiệm ghép đôi 


* 1.5.1 Lệnh gõ và cách đánh dấu đáp án ghép 


* 1.5.2 Một số tuỳ chỉnh 




* 1.6 Bài tự luận 


* 1.6.1 Thêm chức năng cho lệnh `\dapso{}` 


* 1.6.2 Một số tuỳ chỉnh 


* 1.6.3 Bài tập có nhiều ý nhỏ lưu đáp số vắn tắt bằng `dapso` 




* 1.7 Nhóm câu hỏi có chung giả thiết 


* 1.8 Vấn đề tạo mới môi trường để gõ câu hỏi 




* 
**2 Lệnh gọi bảng đáp án (cải tiến)** 


* 2.1 Bảng đáp án dạng biểu bảng nhập azota 


* 2.2 Bảng đáp án có đóng khung 


* 2.3 Bảng đáp án không đóng khung 




* 
**3 Các lệnh, chức năng khác của gói ex-test** 


* 3.1 Lệnh chèn hình `\immini` và `\imminiL` 


* 3.2 Môi trường liệt kê chia cột (`{enumEX}` và `{listEX}`) 


* 3.3 Lệnh `\dotlinefull`, `\dotlineans` và `\dotlineEX` (cải tiến) 


* 3.4 Nhóm lệnh ẩn/hiện nội dung, môi trường (cải tiến) 


* 3.5 Chức năng các tuỳ chọn của gói `ex-test` 


* 3.6 Chức năng trích dẫn nguồn câu hỏi (cải tiến) 


* 3.7 Chức năng đóng khung cho câu hỏi 


* 3.8 Vẽ khoảng, đoạn lên trục số 


* 3.9 Biểu diễn góc lượng giác lên đường tròn lượng giác 





---

1 Cấu trúc và lệnh gõ các loại câu hỏi thông dụng 

1.0 Thiết lập lưu đáp án, lưu lời giải chi tiết 

* 
**Cấu trúc cặp lệnh tạo phạm vi soạn thảo và đặt tên file đáp án:** 



```latex
\Opensolutionfile{ans}[<đường dẫn, tên file lưu đáp án>]
%-----
< các câu hỏi sẽ soạn ở đây >
\Closesolutionfile{ans}

```



* 
**Tác dụng:** lưu đáp án, đáp số vắn tắt cho các câu được gõ trong đó, bao gồm các loại câu hỏi: 


* Trắc nghiệm nhiều lựa chọn (`\choice`). 


* Trắc nghiệm Đúng/Sai (`\choiceTF`). 


* Trắc nghiệm trả lời ngắn (`\shortans`). 


* Bài tập tự luận (`\dapso`). 


* Trắc nghiệm ghép đôi (`\match` `\with`). 





**Chú ý:** 

* Để tách lời giải ra in riêng (kiểu viết sách) thì cần gõ thêm như sau: 



```latex
\Opensolutionfile{ansbook}[<đường dẫn, tên file lưu lời giải>]
\Opensolutionfile{ans}[<đường dẫn, tên file lưu đáp án>]
%------
%----
< các câu hỏi sẽ soạn ở đây >
\Closesolutionfile{ansbook}
\Closesolutionfile{ans}

```



1.1 Câu trắc nghiệm chọn 1 trong nhiều phương án lựa chọn 

```latex
\begin{ex}[<nguồn câu hỏi>][<Các chú thích>][<ID6>]
<Câu dẫn cho câu hỏi nhiều lựa chọn>.
\choice[<tuỳ chọn (nếu cần)>]
% (gõ \True tại phương án đúng đáp án)
{<Phương án A>}
{<Phương án B>}
{<Phương án C>}
{<Phương án D>}
\loigiai{
<Gõ lời giải chi tiết>.
}
\end{ex}

```



* Lệnh `\choice` cũng dùng được cho câu trắc nghiệm có nhiều hơn 4 phương án lựa chọn. 



1.1.1 Các tuỳ chọn của `choice` 

* 
**Một số tuỳ chọn hiển thị phương án của lệnh `choice`:** 


* Mặc định các phương án sẽ được tự động chia cột theo chiều dài tối đa của phương án. 


* 
`choice[1]` để “ép” các phương án xếp theo 1 cột. 


* 
`choice[2]` để “ép” các phương án xếp theo 2 cột. 


* 
`choice[4]` để “ép” các phương án xếp theo 4 cột. 


* 
`\choice[3mm]` để chèn 1 khoảng cao 3mm vào giữa 2 phương án trên và dưới. 





1.1.2 Một số tuỳ chỉnh 

* 
**Khoanh tròn các từ khoá ABCD đầu mỗi phương án:** 


* Đặt dòng lệnh sau đây vào phần khai báo (phía dưới khai báo gói lệnh `{ex_test}`) `\renewcommand{\FalseEX}{\stepcounter{dapan}\circled{\textbf{\Alph{dapan}}}}` 




* 
**Thay đổi dấu “chấm” tự động cuối mỗi phương án:** 


* Đặt lệnh `\def\dotEX{}` vào phía trước lệnh `choice` và sửa theo ý thích. 




* 
**Tăng khoảng cách dọc giữa 2 phương án trên dưới:** 


* Đặt lệnh `\def\parskipchoice{3mm}` vào phía trước lệnh `choice` và sửa chiều cao 3mm thành chiều cao theo ý thích. 




* 
**Thay đổi màu tô cho phương án `True` khi bật tuỳ chọn `[color]` hoặc `[solcolor]`:** 


* Đặt lệnh `\def\colorEX{\color{blue}}` ở phần khai báo và đổi thành màu mình cần. 




* 
**Reset lại số đếm câu hỏi:** 


* Đặt lệnh `\setcounter{ex}{<số liền trước của số muốn bắt đầu lại>}` vào phía trước câu cần đặt lại số thứ tự. 




* 
**Thay đổi cho chữ “Câu” đầu mỗi câu hỏi:** 


* Đặt lệnh `\renewcommand{\nameex}{\color{red}Câu hỏi}` ở phần khai báo. 




* 
**Thay đổi chữ “Lời giải” thành chữ “Hướng dẫn giải":** 


* Đặt lệnh `\def\loigiaiEX{Hướng dẫn giải.}` vào phần khai báo. 




* 
**Thay đổi, ẩn/hiện dòng chữ “Chọn đáp án":** 


* Lệnh luôn ẩn chọn đáp án: `\hidetextchoice` 


* Lệnh luôn hiện chọn đáp án: `\showtextchoice` 


* Lệnh sửa chữ Chọn đáp án: `\def\selectchoice{Chọn đáp án}` 




* 
**Thay đổi cách trích dẫn nguồn đề thi:** 


* Nội dung câu hỏi tự động xuống dòng với các câu có trích dẫn nguồn: `\OPTN{exbreak=1}` 


* Trích dẫn nguồn câu hỏi để ở cuối câu hỏi: `\OPTN{explain=1}` 





1.1.3 Gõ câu trắc nghiệm với đặc trưng riêng của môn tiếng Anh 

**Ví dụ 1.** Yoghurt, one of the healthiest snacks, are advised for people with daily calcium needs. A. one of B. healthiest C. are D. daily 

* Cần gạch chân và ghi từ khoá phương án cho cụm từ nào trong câu thì `\choice{<cụm từ đó>}`. 


* Vẫn dùng lệnh `\True` để đánh dấu đáp án. Trong ví dụ trên, có 4 lệnh `choice` được gõ, gồm: 


* 
`\choice{one of}` 


* 
`\choice{healthiest}` 


* 
`\choice{\True are}` 


* 
`\choice{daily}` 





1.2 Câu trắc nghiệm được chọn 1 hoặc nhiều hơn 1 phương án 

* Thay vì dùng lệnh `\choice` thì dùng lệnh `\choiceN` (thêm ký tự N viết hoa vào). 


* Mọi vấn đề khác về các tuỳ chọn ... đều tương tự như cách gõ câu chọn 1 phương án. 


* Khi đó từ khoá đầu mỗi phương án không dùng A.B.C.D. mà đổi thành 1) 2) 3) 4), điều này giúp học sinh hạn chế nhầm lẫn về số lượng phương án được chọn trong câu hỏi. 



1.3 Câu trắc nghiệm Đúng/Sai 

```latex
\begin{ex}[<nguồn câu hỏi>][<Các chú thích>] %[<ID6>]
<Câu dẫn cho câu hỏi có 4 phát biểu lựa chọn Đúng/Sai>.
\choiceTF[<tuỳ chọn (nếu cần)>]
% (gõ \True tại phát biểu đúng)
{<Phát biểu 1>}
{<Phát biểu 2>}
{<Phát biểu 3>}
{<Phát biểu 4>}
\loigiai{
<Phần trình bày, giới thiệu chung (nếu có)>
\begin{itemchoice}
\itemch <Lời giải cho phát biểu 1>.
\itemch <Lời giải cho phát biểu 2>.
\itemch <Lời giải cho phát biểu 3>.
\itemch <Lời giải cho phát biểu 4>.
\end{itemchoice}
}
\end{ex}

```



* Lệnh `\choiceTF` cũng dùng được cho câu đúng sai có nhiều hơn 4 phát biểu. 


Dưới đây là phần tiếp theo của bản chuyển thể Markdown từ tài liệu **Huong-dan-ex-test-v3.1.pdf**, tiếp tục từ mục 1.3.1 đến hết mục 1.8.

---

#### 1.3.1 Các tuỳ chọn của `choiceTF`

* **Một số tuỳ chọn hiển thị các phát biểu của lệnh `\choiceTF`:**

* Mặc định các phát biểu hiển thị dạng chuẩn đề thi 2025 và tự động chia cột.


* `choiceTF[1]`: các phát biểu hiển thị dạng chuẩn đề thi 2025 bị “ép” thành 1 cột.


* `choiceTF[2]`: các phát biểu hiển thị dạng chuẩn đề thi 2025 bị “ép” thành 2 cột.


* `choiceTF[4]`: các phát biểu hiển thị dạng chuẩn đề thi 2025 bị “ép” thành 4 cột.


* `\choiceTF[3mm]`: phát biểu hiển thị dạng chuẩn đề thi 2025, tự động chia cột và được thêm khoảng cách dọc **3mm** vào giữa 2 phát biểu trên và dưới.




* **Các tuỳ chọn hiển thị 4 phát biểu Đúng/Sai vào trong biểu bảng:**

* `choiceTF[t]`: hiển thị 1 bảng hoặc tự động tách 2 bảng Đúng/Sai theo chiều dài phát biểu.


* `choiceTF[1t]`: hiển thị 1 bảng Đúng/Sai có 4 phát biểu.


* `choiceTF[2t]`: hiển thị 2 bảng Đúng/Sai, mỗi bảng có 2 phát biểu.





#### 1.3.2 Đồng bộ tuỳ chọn cho `choiceTF` toàn tài liệu



* Dù các câu Đúng/Sai trên tài liệu có nhiều cách hiển thị khác nhau (dạng bảng, dạng chuẩn,...), chỉ cần dùng cách dưới đây tất cả các câu Đúng/Sai sẽ được đồng nhất cách hiển thị.


* Đặt lệnh `\OPTN{...}` chứa các tuỳ chọn cần đồng bộ ở đầu tài liệu, tức gần `\begin{document}` (và không có thêm vị trí nào khác được đặt lệnh `\OPTN`).


* **Mặc định:** `\OPTN{kindTF=, dapanTF=a, boldTF=0, phatbieu=Phát biểu, viettat=1, sepTF=), addanswers=1, addquestions=0}`


**Chi tiết các tuỳ chọn gồm có:**

* **`kindTF`:**

* `kindTF=0`: tuỳ chọn hiển thị dạng chuẩn đề thi 2025.


* `kindTF=1t`: tuỳ chọn hiển thị dạng 1 biểu bảng.


* `kindTF=2t`: tuỳ chọn hiển thị dạng 2 biểu bảng.


* `kindTF=t`: tuỳ chọn tự động hiển thị 1 bảng hoặc 2 bảng.


* `kindTF=t0`: tuỳ chọn bỏ dòng tiêu đề và bỏ 2 cột chọn Đúng/Sai trong biểu bảng.


* `kindTF=t01`: tuỳ chọn bỏ dòng tiêu đề và có 2 cột chọn Đúng/Sai trong biểu bảng.


* `kindTF=t10`: tuỳ chọn có dòng tiêu đề và bỏ 2 cột chọn Đúng/Sai trong biểu bảng.


* `kindTF=t1`: tuỳ chọn nhập 2 cột Đúng/Sai thành 1 cột duy nhất.


* `kindTF=` (để trống): trở lại áp dụng tuỳ chọn riêng của mỗi câu.




* **`dapanTF`:**

* `dapanTF=a`: tuỳ chọn các ý đúng - sai có thứ tự là a) b) c) d).


* `dapanTF=1`: tuỳ chọn các ý đúng - sai có thứ tự là 1) 2) 3) 4).


* `dapanTF=A`: tuỳ chọn các ý đúng - sai có thứ tự là A. B. C. D..




* **`boldTF`:**

* `boldTF=1`: tuỳ chọn tiêu đề các cột của bảng đúng - sai được in đậm.


* `boldTF=0`: tuỳ chọn tiêu đề các cột của bảng đúng - sai không in đậm.




* **`phatbieu`:** `phatbieu=Phát biểu` dùng để sửa tiêu đề của 4 phát biểu.


* **`viettat`:**

* `viettat=0`: tuỳ chọn không viết tắt chữ “Đúng” và “Sai”.


* `viettat=1`: tuỳ chọn viết tắt chữ Đúng và Sai thành “Đ” và “S”.




* **`sepTF`:** `sepTF=)` phân tách giữa các ký tự ký hiệu ý hỏi (a, b, c, d) với các phát biểu bởi dấu `)`.


* **`addanswers`:** `addanswers=1` tuỳ chọn tự động thêm ký hiệu Đúng hoặc Sai vào mỗi lời giải chi tiết bên trong môi trường `{itemchoice}`.


* **`addquestions`:** `addquestions=1` tuỳ chọn tự động thêm đề bài (nội dung phát biểu Đúng/Sai) vào đầu mỗi lời giải chi tiết bên trong môi trường `{itemchoice}`.



> Lưu ý: Những tuỳ chọn không cần điều chỉnh thì không cần liệt kê vào lệnh `\OPTN`.
> 
> 

#### 1.3.3 Một số tuỳ chỉnh



* Sửa định dạng các từ khoá a) b) c) d) đầu mỗi phát biểu bằng các dòng lệnh:



```latex
\renewcommand{\FalseTF}{\stepcounter{dapan}\textbf{\DapAnTF\sepTF}}
\renewcommand{\TrueTF}{\stepcounter{dapan}\squareEX{\bf\DapAnTF}}

```

* Ở dạng bảng, có thể dùng lệnh `\renewcommand{\arraystretch}{<một số>}` để thay đổi khoảng cách giữa các hàng trong bảng.


* Các tuỳ chỉnh hiển thị khác được thực hiện tương tự tuỳ chỉnh cho câu 4 lựa chọn:


* `\def\dotEX{}`

* `\def\parskipchoice{3mm}`

* `\def\colorEX{\color{blue}}`

* `\setcounter{ex}{<số liền trước của số muốn bắt đầu lại>}`

* `\renewcommand{\nameex}{\color{red}Câu hỏi}`

* `\def\loigiaiEX{Hướng dẫn giải.}`

* `\hidetextchoice`

* `\showtextchoice`

* `\def\selectchoiceTF{Chọn đáp án}`




---

### 1.4 Câu trắc nghiệm trả lời ngắn



```latex
\begin{ex}[<nguồn câu hỏi>][<Các chú thích>] %[<ID6>]
<Câu hỏi dạng trả lời ngắn>.
\shortans[<tuỳ chọn (nếu cần)>]{<đáp số>}
\loigiai{
<Gõ lời giải chi tiết>.
}
\end{ex}

```

> Thêm `\par` kề trước `\shortans` nếu ô để nhập kết quả không nằm cùng dòng cuối của đề bài.
> 
> 

#### 1.4.1 Các tuỳ chọn của `shortans`

* **Một số tuỳ chọn hiển thị chỗ nhập kết quả của lệnh `\shortans`:**

* Mặc định hiển thị ô điền kết quả dài **4cm**.


* `shortans[oly]`: hiển thị 4 ô vuông để học sinh tập tách ký tự của kết quả.


* `shortans[...]`: hiển thị đoạn dòng chấm dài **4cm** để điền kết quả ở cuối câu hỏi.


* `shortans[3]`: hiển thị ô có chiều dài **3cm** để điền kết quả cuối câu hỏi.


* `shortans[0]`: dạng chuẩn đề thi 2025 (không có chỗ điền kết quả).





#### 1.4.2 Đồng bộ tuỳ chọn cho `shortans` toàn tài liệu



* Dù các câu Trả lời ngắn trên tài liệu có nhiều cách hiển thị khác nhau (dạng điền vào ô trống, dạng chuẩn đề thi 2025, điền vào 4 ô ly,...), chỉ cần đặt cấu trúc đồng bộ ở đầu tài liệu, gần `\begin{document}`.


* **Mặc định:** `\OPTN{kindSA=, ketquaSA=KQ:, widthSA=4, heightSA=0.9, dapanSA=a}`


**Chi tiết các tuỳ chọn gồm có:**

* `kindSA=0`: tuỳ chọn hiển thị dạng chuẩn đề thi 2025.


* `kindSA=oly`: tuỳ chọn hiển thị dạng 4 ô ly tách ký tự.


* `kindSA=...`: tuỳ chọn hiển thị dạng dòng chấm cho chỗ điền kết quả.


* `kindSA=n` (với $ n $ là một số): tuỳ chọn hiển thị ô điền kết quả dài $ n $ cm.


* `kindSA=` (để trống): tuỳ chọn giữ hiển thị riêng thiết lập của mỗi câu hỏi.


* `ketquaSA=KQ:` tuỳ chọn dùng để sửa chữ phía trước ô điền kết quả.


* `widthSA=4`: mặc định chiều dài của ô điền kết quả là **4cm**.


* `heightSA=0.9`: mặc định chiều cao của ô điền kết quả là **0.9cm**.


* `dapanSA=a`: thứ tự ý nhỏ của câu trên bảng đáp án là a) b) c) d).


* `dapanSA=1`: thứ tự ý nhỏ của câu trên bảng đáp án là 1) 2) 3) 4).


* `dapanSA=A`: thứ tự ý nhỏ của câu trên bảng đáp án là A. B. C. D..



#### 1.4.3 Một số tuỳ chỉnh



* Các tuỳ chỉnh khác thực hiện tương tự như câu hỏi nhiều lựa chọn:


* `\setcounter{ex}{<số liền trước>}`

* `\renewcommand{\nameex}{\color{red}Câu hỏi}`

* `\def\loigiaiEX{Hướng dẫn giải.}`

* `\def\selectshortans{Đáp án:}`




#### 1.4.4 Câu hỏi có nhiều ý nhỏ trả lời ngắn bằng `shortans`

* Một câu hỏi có nhiều ý nhỏ trả lời ngắn có thể sử dụng môi trường danh sách `{listEX}` (tất cả các `\item` đều phải đặt kèm lệnh `\shortans`):



```latex
\begin{listEX}
\item Ý hỏi thứ 1 \shortans[<tùy chọn>]{<kết quả 1>}
\item Ý hỏi thứ 2 \shortans[<tùy chọn>]{<kết quả 2>}
\item Ý hỏi thứ 3 \shortans[<tùy chọn>]{<kết quả 3>}
\end{listEX}

```

* Mặc định thứ tự của đáp án trong danh sách đáp án là a) b) c) d). Muốn đổi kiểu đánh thứ tự chữ cái thành đánh số thì dùng lệnh `\dapanSA{\arabic{dapan}}` hoặc khai báo `\OPTN{dapanSA=1}`.



---

### 1.5 Câu trắc nghiệm ghép đôi



```latex
\begin{ex}[<nguồn câu hỏi>][<Các chú thích>][<ID6>]
<Nội dung câu dẫn, giả thiết chung....>.
\match
{<Phát biểu 1>}
{<Phát biểu 2>}
{<Phát biểu 3>}
{<Phát biểu 4>}
\with
[3] {<ý ghép của phát biểu 3>}
[1] {<ý ghép của phát biểu 1>}
[4] {<ý ghép của phát biểu 4>}
{<ý ghép thừa>}
[2] {<ý ghép của phát biểu 2>}
{<ý ghép thừa>}
\loigiai{
<Phần trình bày, giới thiệu chung (nếu có)>
\begin{itemchoice}
\itemch <Lời giải cho phát biểu 1>.
\itemch <Lời giải cho phát biểu 2>.
\itemch <Lời giải cho phát biểu 3>.
\itemch <Lời giải cho phát biểu 4>.
\end{itemchoice}
}
\end{ex}

```

#### 1.5.1 Lệnh gõ và cách đánh dấu đáp án ghép



* Số phát biểu ở `\match` tối đa là 10 và số ý ghép ở `\with` không giới hạn, thỏa mãn 2 điều kiện:


1. Số phát biểu ở lệnh `\match` không được nhiều hơn số ý ghép ở lệnh `\with`.


2. Các phát biểu đều có ý ghép tương ứng và mỗi ý ghép chỉ ghép với duy nhất 1 phát biểu.




* **Lưu ý về lệnh `\match`:**

* Các phát biểu trong `\match` sẽ được tự động lưu số thứ tự 1, 2, 3,... theo đúng thứ tự gõ để hỗ trợ đánh dấu đáp án.


* Khi trộn trắc nghiệm, nếu `\match` được gõ mặc định thì **không được đảo thứ tự các phát biểu** vì sẽ làm sai lệch đáp án ghép.


* Nếu gõ thủ công thêm số thứ tự cho tất cả các phát biểu, ví dụ `[1] {<Phát 1 biểu>}`, thì khi đảo các phát biểu kèm số thứ tự đó, đáp án ghép sẽ không bị sai.




* **Lưu ý về lệnh `\with`:**

* Dùng `[số thứ tự của Phát biểu]` đặt phía trước `{<ý ghép của phát biểu đó>}`.


* Không thêm gì vào phía trước các `{<ý ghép thừa>}`.


* Việc đảo các `{<ý ghép>}` kèm theo `[số thứ tự]` kề trước nó khi trộn đề sẽ không làm sai đáp án ghép (bất kể lệnh `\match` được gõ mặc định hay gõ thủ công).





#### 1.5.2 Một số tuỳ chỉnh



Các từ ngữ và cách hiển thị trên bảng ghép đôi được cấu hình qua lệnh `\OPTN` đặt ở đầu tài liệu gần `\begin{document}`.

* **Mặc định:**


```latex
\OPTN{
chidan={Ghép mỗi phát biểu ở cột I với một ý ghép ở cột II để được mệnh đề đúng},
tieudeMW=1, boldMW=1, cotI={Cột I}, cotII={Cột II}, debaiMW=1, dapanMW=A,
TabCS=2mm, parskipI=1mm, parskipII=1mm, length=1, lengthII=0.25,
ketqua={Kết quả ghép nối:}
}

```

**Chi tiết các tuỳ chọn gồm có:**

* `chidan`: Dòng chỉ dẫn học sinh cách làm bài, hiển thị kề trên bảng ghép nối 2 cột. Nếu để trống (`chidan=`) thì không hiển thị dòng chỉ dẫn.


* `tieudeMW=1`: Hiển thị dòng tiêu đề của bảng ghép nối (`tieudeMW=0` để ẩn).


* `boldMW=1`: In đậm dòng tiêu đề (`boldMW=0` để bỏ in đậm).


* `cotI=Cột I` và `cotII=Cột II`: Sửa nội dung tiêu đề hiển thị ở Cột I và Cột II.


* `debaiMW`: Thứ tự đánh cho các phát biểu ở cột I. Khai báo `=1` (đánh số 1,2,3...), `=A` (đánh chữ hoa A,B,C...), hoặc `=a` (đánh chữ thường a,b,c...).


* `dapanMW`: Thứ tự đánh cho các ý ghép ở cột II (tương tự `debaiMW`).


* `TabCS=2mm`: Khoảng cách ngang giữa văn bản và đường kẻ dọc của bảng ghép nối.


* `parskipI=1mm` và `parskipII=1mm`: Khoảng cách dọc giữa các dòng ở cột I và cột II.


* `length=1`: Chiều rộng tổng thể của bảng ghép nối bằng 1 `linewidth`.


* `lengthII=0.25`: Chiều rộng của Cột II chiếm 0.25 chiều rộng của toàn bảng.


* `ketqua`: Dòng văn bản hiển thị phía dưới bảng để học sinh điền kết quả.



> Để chỉnh sửa tuỳ chọn riêng cho một câu cụ thể, dùng lệnh `\def\<loại tuỳ chọn>{nội dung}` đặt kề trên lệnh `\match` (Ví dụ: `\def\parskipI{4mm}`, `\def\lengthII{0.6}`).
> 
> 

---

### 1.6 Bài tự luận



```latex
\begin{bt}[<nguồn câu hỏi>][<Các chú thích>] %[<ID6>]
<Nội dung câu hỏi tự luận>.
\dapso[tuỳ chọn]{<đáp số vắn tắt>}
\loigiai{
<Gõ lời giải chi tiết>.
}
\end{bt}

```

#### 1.6.1 Thêm chức năng cho lệnh `\dapso{}`

* Lệnh `\dapso{<kết quả>}` hiển thị đáp số vắn tắt đặt ở cuối câu hỏi tự luận.


* Lệnh đã được cập nhật tính năng tự động lưu đáp số vắn tắt vào file đáp án tương tự như các lệnh `\choice`, `\choiceTF`, `\shortans`, `\match`.



#### 1.6.2 Một số tuỳ chỉnh



* **Ẩn đáp số vắn tắt:** Đặt lệnh `\exitdapso` hoặc `\hidedapso` ở đầu tài liệu. Khi cần bật hiển thị lại ở các phần bên dưới, sử dụng lệnh `\showdapso`.


* Các tuỳ chỉnh hiển thị khác tương tự câu hỏi trắc nghiệm:


* `\setcounter{bt}{<số liền trước>}`

* `\renewcommand{\namebt}{\color{blue}Bài tập}`

* `\def\loigiaiEX{Hướng dẫn giải.}`

* `\def\chudapso{DS:}` hoặc `\OPTN{chudapso=DS}`




#### 1.6.3 Bài tập có nhiều ý nhỏ lưu đáp số vắn tắt bằng `dapso`

* Có thể kết hợp môi trường danh sách `{listEX}` cho các bài tập gồm nhiều ý nhỏ hỏi đáp số vắn tắt (mọi `\item` đều phải chứa lệnh `\dapso`):



```latex
\begin{listEX}
\item Ý hỏi thứ 1 \dapso[<kiểu thứ tự đáp án>]{đáp số vắn tắt 1}
\item Ý hỏi thứ 2 \dapso[<kiểu thứ tự đáp án>]{đáp số vắn tắt 2}
\item Ý hỏi thứ 3 \dapso[<kiểu thứ tự đáp án>]{đáp số vắn tắt 3}
\end{listEX}

```


(Ý hỏi nào không có đáp số vắn tắt vẫn phải nhập lệnh rỗng `\dapso{}`).

* **Kiểu thứ tự trong bảng đáp án:** Mặc định là chữ cái thường `a) b) c)`. Bạn có thể thay đổi bằng tuỳ chọn `[1]` để đánh số `1) 2) 3)` hoặc `[A]` để đánh chữ hoa `A) B) C)`.



---

### 1.7 Nhóm câu hỏi có chung giả thiết



```latex
\begin{ex}[<nguồn câu hỏi>][<Các chú thích>] %[<ID6>]
\sochc{<số câu hỏi con>}
<Giả thiết chung cho các câu hỏi con bên dưới>
\begin{chc}
Nội dung câu hỏi con thứ nhất.
\loigiai{
<Lời giải câu hỏi con thứ nhất>
}
\end{chc}
\begin{chc}
Nội dung câu hỏi con thứ hai.
\loigiai{
<Lời giải câu hỏi con thứ hai>
}
\end{chc}
\end{ex}

```

* Nếu không sử dụng lệnh `\sochc{}`, các câu hỏi con mặc định hiển thị theo dạng các tiểu mục chữ cái `a) b) c)`.


* Lệnh `\sochc{}` (đặt ngay dưới `\begin{ex}`) giúp định dạng nhóm câu hỏi chung giả thiết hiển thị theo kiểu đề Đánh giá năng lực của ĐHQG-HCM.


* Muốn thay đổi lời dẫn mặc định đầu nhóm, truyền thêm tham số tuỳ chọn: `\sochc[Nội dung lời dẫn mới]{<số câu hỏi con>}`.



---

### 1.8 Vấn đề tạo mới môi trường để gõ câu hỏi



Môi trường `{ex}` và `{bt}` là hai môi trường mặc định có sẵn. Để tạo một môi trường gõ câu hỏi hoàn toàn mới nhưng vẫn thừa hưởng đầy đủ chức năng của gói `ex-test`, thực hiện khai báo tuần tự các lệnh sau ở phần tiền sảnh:

1. **Khai báo môi trường:** `\newtheorem{<tên môi trường mới>}{<tiêu đề>}`

2. **Khai báo chức năng làm đáp án:** `\fixshowans{<tên môi trường vừa đặt>}`

3. **Khai báo tương thích danh sách:** `\listenumerate{<tên môi trường vừa đặt>}`

Dưới đây là phần tiếp theo của bản chuyển thể Markdown từ tài liệu **Huong-dan-ex-test-v3.1.pdf**, bao gồm các mục từ 2.0 đến hết tài liệu.

---

## 2 Lệnh gọi bảng đáp án (cải tiến)

Lệnh gọi bảng đáp án được thực hiện sau lệnh `\Closesolutionfile{ans}`.

### 2.1 Bảng đáp án dạng biểu bảng nhập azota

* **Lệnh gõ:** `\viewansazota{ans}`.
* **Đặc điểm:** Tự động tạo bảng đáp án có định dạng cột và hàng tương thích để chụp ảnh hoặc copy dữ liệu vào hệ thống Azota.

### 2.2 Bảng đáp án có đóng khung

* **Lệnh gõ:** `\viewans[<số cột>]{ans}`.
* **Tùy chọn:**
* `<số cột>`: Số cột hiển thị của bảng đáp án (mặc định là 10).
* Đáp án của câu trắc nghiệm nhiều lựa chọn sẽ được in đậm.
* Đáp án của câu Đúng/Sai được liệt kê theo dạng `1-Đ, 2-S...`.
* Kết quả câu Trả lời ngắn và Tự luận được liệt kê vắn tắt.



### 2.3 Bảng đáp án không đóng khung

* **Lệnh gõ:** `\viewans*{ans}`.
* **Đặc điểm:** Hiển thị danh sách đáp án dưới dạng văn bản thuần, phân cách bởi dấu phẩy, phù hợp để tiết kiệm diện tích trang in.

---

## 3 Các lệnh, chức năng khác của gói ex-test

### 3.1 Lệnh chèn hình `\immini` và `\imminiL`

Sử dụng để chèn hình ảnh nằm bên cạnh văn bản (thay thế cho gói `wrapfig` thường gây lỗi đè chữ).

* **Lệnh gõ:**

```latex
\immini[<khoảng cách>]{<Văn bản>}{<Lệnh vẽ hình hoặc chèn ảnh>}
\imminiL[<khoảng cách>]{<Lệnh vẽ hình hoặc chèn ảnh>}{<Văn bản>}

```

* **Tùy chọn:**
* `\immini`: Hình bên phải, chữ bên trái.
* `\imminiL`: Hình bên trái, chữ bên phải.
* `<khoảng cách>`: Độ rộng dành cho phần hình ảnh (ví dụ: `5cm`).



### 3.2 Môi trường liệt kê chia cột (`{enumEX}` và `{listEX}`)

Giúp liệt kê các mục và tự động chia cột dựa trên độ dài nội dung.

* **`{enumEX}[<số cột>]`:** Đánh số thứ tự tự động (1, 2, 3...).
* **`{listEX}[<số cột>]`:** Đánh dấu theo ký tự (a, b, c...).
* **Tùy chọn:** Nếu không điền số cột, gói lệnh sẽ tự tính toán số cột tối ưu.

### 3.3 Lệnh `\dotlinefull`, `\dotlineans` và `\dotlineEX` (cải tiến)

* **`\dotlinefull{<số dòng>}`:** Tạo các dòng chấm hết chiều rộng trang giấy.
* **`\dotlineans{<số dòng>}`:** Tạo dòng chấm nhưng chừa trống một khoảng ở đầu dòng đầu tiên (thường dùng sau chữ "Lời giải:").
* **`\dotlineEX{<độ dài>}`:** Tạo một đoạn dòng chấm với độ dài tùy ý.

### 3.4 Nhóm lệnh ẩn/hiện nội dung, môi trường (cải tiến)

* **`\hideans` / `\showans`:** Ẩn hoặc hiện đáp án của các câu hỏi.
* **`\hideloi` / `\showloi`:** Ẩn hoặc hiện lời giải chi tiết.
* **`\hideall`:** Ẩn cả lời giải và đáp số để tạo bản in đề bài thuần túy.

### 3.5 Chức năng các tuỳ chọn của gói `ex-test`

Khai báo khi gọi gói lệnh: `\usepackage[<tùy chọn>]{ex_test}`.

* **`color`:** Tô màu đáp án đúng trong đề bài.
* **`solcolor`:** Tô màu đáp án đúng trong phần lời giải.
* **` booklet`:** Tự động định dạng tài liệu theo dạng sách bài tập.
* **`nosol`:** Không in lời giải chi tiết.

### 3.6 Chức năng trích dẫn nguồn câu hỏi (cải tiến)

Nguồn câu hỏi đặt trong dấu `[]` đầu tiên của môi trường `ex` hoặc `bt`.

* Để ẩn toàn bộ nguồn câu hỏi: dùng lệnh `\hidepoint`.
* Để hiện lại: dùng lệnh `\showpoint`.

### 3.7 Chức năng đóng khung cho câu hỏi

Sử dụng môi trường `bclogo` hoặc các lệnh tùy biến để bao quanh câu hỏi. Gói `ex-test` hỗ trợ lệnh `\boxex{<nội dung>}` để đóng khung nhanh.

### 3.8 Vẽ khoảng, đoạn lên trục số

* **Lệnh gõ:** `\trục số[<tùy chọn>]{<danh sách các điểm>}`.
* Tự động vẽ trục số và biểu diễn các tập hợp số (ngoặc tròn, ngoặc vuông) theo đúng quy chuẩn toán học.

### 3.9 Biểu diễn góc lượng giác lên đường tròn lượng giác

* **Lệnh gõ:** `\tròn lượng giác[<tùy chọn>]{<góc>}`.
* Hỗ trợ vẽ đường tròn đơn vị, các trục $ \sin $, $ \cos $, và biểu diễn cung lượng giác tương ứng với số đo nhập vào.

---

**HẾT TÀI LIỆU**