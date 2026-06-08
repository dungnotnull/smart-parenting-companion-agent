from backend.services.age_stage_mapper import AgeStage, WHO_MILESTONES, ERIKSON_STAGE, PIAGET_STAGE, STAGE_GUIDANCE

VI_STAGE_LABELS: dict[AgeStage, str] = {
    AgeStage.NEWBORN: "sơ sinh",
    AgeStage.INFANT: "nhũ nhi",
    AgeStage.TODDLER: "tập đi",
    AgeStage.PRESCHOOL: "mẫu giáo",
    AgeStage.SCHOOL_AGE: "tiểu học",
    AgeStage.EARLY_ADOLESCENT: "đầu thanh thiếu niên",
    AgeStage.LATE_ADOLESCENT: "cuối thanh thiếu niên",
    AgeStage.ADULT: "trưởng thành",
}

VI_MILESTONES: dict[AgeStage, list[str]] = {
    AgeStage.NEWBORN: [
        "Phản ứng với âm thanh",
        "Phản xạ bú và tìm vú còn nguyên vẹn",
        "Tập trung nhìn mặt người ở khoảng cách 20-30 cm",
        "Phản xạ giật mình (Moro) có mặt",
    ],
    AgeStage.INFANT: [
        "Lật được hai chiều (~6 tháng)",
        "Ngồi không cần hỗ trợ (~6-8 tháng)",
        "Bò (~7-10 tháng)",
        "Đứng vịn (~9-12 tháng)",
        "Từ đầu tiên (~12 tháng)",
        "Cầm nhón (~10-12 tháng)",
        "Sợ người lạ (~8-10 tháng)",
    ],
    AgeStage.TODDLER: [
        "Đi độc lập (~12-15 tháng)",
        "Leo cầu thang có trợ giúp (~18-24 tháng)",
        "Sử dụng 10-50 từ (~18-24 tháng)",
        "Cụm 2 từ (~24 tháng)",
        "Chơi giả vờ xuất hiện",
        "Tự xúc ăn bằng thìa",
        "Sẵn sàng tập đi vệ sinh (~24-36 tháng)",
    ],
    AgeStage.PRESCHOOL: [
        "Nhảy và đứng một chân (~4 tuổi)",
        "Vẽ người có 2-4 bộ phận",
        "Chơi hợp tác với bạn",
        "Làm theo hướng dẫn 3 bước",
        "Kể chuyện đơn giản",
        "Đếm đến 10",
        "Hiểu khái niệm quá khứ/tương lai",
    ],
    AgeStage.SCHOOL_AGE: [
        "Đọc độc lập (~6-7 tuổi)",
        "Hiểu bảo toàn (giai đoạn Piaget)",
        "Kết bạn với bạn cùng trang lứa",
        "Phát triển tư duy logic",
        "Hiểu về quy tắc và công bằng",
        "Tăng tính độc lập trong tự chăm sóc",
    ],
    AgeStage.EARLY_ADOLESCENT: [
        "Thay đổi dậy thì bắt đầu",
        "Suy luận trừu tượng phát triển",
        "Quan hệ bạn bè thân thiết hơn",
        "Bắt đầu khám phá bản sắc",
        "Tâm trạng thay đổi nhiều hơn",
    ],
    AgeStage.LATE_ADOLESCENT: [
        "Suy luận trừu tượng nâng cao",
        "Lập kế hoạch và đặt mục tiêu tương lai",
        "Quan hệ thân mật sâu sắc hơn",
        "Lý luận đạo đức trưởng thành",
        "Khám phá nghề nghiệp và hướng sống",
    ],
    AgeStage.ADULT: [
        "Trưởng thành nhận thức hoàn toàn (thùy trán ~25 tuổi)",
        "Kỹ năng sống độc lập",
        "Tập trung ổn định nghề nghiệp và quan hệ",
    ],
}

VI_ERIKSON_STAGE: dict[AgeStage, str] = {
    AgeStage.NEWBORN: "Tin tưởng vs. Nghi ngờ (0-18 tháng)",
    AgeStage.INFANT: "Tin tưởng vs. Nghi ngờ → Tự chủ vs. Xấu hổ/Nghi ngờ (18 tháng-3 tuổi)",
    AgeStage.TODDLER: "Tự chủ vs. Xấu hổ/Nghi ngờ (18 tháng-3 tuổi)",
    AgeStage.PRESCHOOL: "Chủ động vs. Tội lỗi (3-5 tuổi)",
    AgeStage.SCHOOL_AGE: "Siêng năng vs. Tự ti (6-11 tuổi)",
    AgeStage.EARLY_ADOLESCENT: "Bản sắc vs. Nhầm lẫn vai trò (12-18 tuổi)",
    AgeStage.LATE_ADOLESCENT: "Bản sắc vs. Nhầm lẫn vai trò → Thân mật vs. Cô lập",
    AgeStage.ADULT: "Thân mật vs. Cô lập (thanh niên)",
}

VI_PIAGET_STAGE: dict[AgeStage, str] = {
    AgeStage.NEWBORN: "Cảm giác-Vận động (0-2 tuổi)",
    AgeStage.INFANT: "Cảm giác-Vận động (0-2 tuổi)",
    AgeStage.TODDLER: "Cảm giác-Vận động → Tiền thao tác (2-7 tuổi)",
    AgeStage.PRESCHOOL: "Tiền thao tác (2-7 tuổi)",
    AgeStage.SCHOOL_AGE: "Thao tác cụ thể (7-11 tuổi)",
    AgeStage.EARLY_ADOLESCENT: "Thao tác hình thức (12+ tuổi)",
    AgeStage.LATE_ADOLESCENT: "Thao tác hình thức (12+ tuổi)",
    AgeStage.ADULT: "Thao tác hình thức (12+ tuổi)",
}

VI_STAGE_GUIDANCE: dict[AgeStage, str] = {
    AgeStage.NEWBORN: (
        "Tập trung vào chăm sóc đáp ứng, thiết lập nhịp điệu ăn và ngủ, "
        "tiếp xúc da kề da, và nhận biết tín hiệu của trẻ sơ sinh. "
        "Cha mẹ nên ưu tiên phục hồi sau sinh và sức khỏe tâm thần."
    ),
    AgeStage.INFANT: (
        "Khuyến khích chơi trên sàn, tập nằm sấp, cho ăn đáp ứng (sữa mẹ hoặc sữa công thức), "
        "giới thiệu thức ăn bổ sung lúc 6 tháng, và thực hành ngủ an toàn. "
        "Gắn bó cha mẹ-con là động lực phát triển chính."
    ),
    AgeStage.TODDLER: (
        "Hỗ trợ tự chủ trong giới hạn an toàn. Sử dụng kỷ luật tích cực và chuyển hướng "
        "thay vì trừng phạt. Môi trường giàu ngôn ngữ là quan trọng. "
        "Thói quen nhất quán giảm tranh giành quyền lực."
    ),
    AgeStage.PRESCHOOL: (
        "Khuyến khích tò mò, chơi tưởng tượng, và kỹ năng xã hội sớm. Đặt giới hạn rõ ràng "
        "với sự ấm áp. Sẵn sàng đi học bao gồm tự điều chỉnh hơn là kỹ năng học thuật. "
        "Theo dõi tương tác với bạn bè."
    ),
    AgeStage.SCHOOL_AGE: (
        "Hỗ trợ phát triển học tập trong khi bảo tồn động lực nội tại. Cân bằng cấu trúc "
        "với chơi tự do. Hướng dẫn kỹ năng kết bạn và giải quyết xung đột. "
        "Theo dõi chất lượng và số lượng thời gian màn hình."
    ),
    AgeStage.EARLY_ADOLESCENT: (
        "Tôn trọng sự tự chủ đang phát triển trong khi duy trì kết nối. Lắng nghe nhiều hơn giảng dạy. "
        "Hỗ trợ khám phá bản sắc. Theo dõi sức khỏe tâm thần (dấu hiệu trầm cảm, lo âu). "
        "Thảo luận về thay đổi dậy thì một cách cởi mở và tích cực."
    ),
    AgeStage.LATE_ADOLESCENT: (
        "Chuyển từ quản lý sang huấn luyện/tư vấn. Hỗ trợ lập kế hoạch tương lai "
        "trong khi để thanh thiếu niên dẫn dắt. Tôn trọng riêng tư. "
        "Tiếp tục theo dõi sức khỏe tâm thần. Thảo luận về hành vi rủi ro "
        "trong khuôn khổ giảm thiểu tác hại."
    ),
    AgeStage.ADULT: (
        "Cung cấp tài nguyên và hỗ trợ khi được yêu cầu. Tôn trọng hoàn toàn sự tự chủ. "
        "Tập trung vào thách thức chuyển tiếp sang tuổi trưởng thành: tài chính, nghề nghiệp, quan hệ."
    ),
}

VI_VACCINATION_SCHEDULE = {
    "Sơ sinh": "BCG (lao), Viêm gan B (mũi 1)",
    "2 tháng": "DPT-VGB-Hib (5 trong 1, mũi 1), Bại liệt (OPV, mũi 1)",
    "3 tháng": "DPT-VGB-Hib (mũi 2), Bại liệt (OPV, mũi 2)",
    "4 tháng": "DPT-VGB-Hib (mũi 3), Bại liệt (OPV, mũi 3)",
    "9 tháng": "Sởi (mũi 1), Sởi-Rubella (một số tỉnh)",
    "12 tháng": "Viêm não Nhật Bản (mũi 1)",
    "13 tháng": "Viêm não Nhật Bản (mũi 2)",
    "18 tháng": "DPT nhắc lại, Sởi-Rubella (mũi 2)",
}

VI_EMERGENCY_RESPONSE = (
    "⚠️ **Đây có thể là tình huống cấp cứu y tế.**\n\n"
    "Hãy **dừng sử dụng chat này ngay lập tức** và:\n"
    "- Gọi **115** hoặc số cấp cứu địa phương\n"
    "- Đến **khoa cấp cứu bệnh viện** gần nhất\n"
    "- Liên hệ **bác sĩ nhi khoa** của bạn ngay\n\n"
    "Trợ lý AI này không được trang bị để xử lý tình huống cấp cứu y tế. "
    "An toàn của con bạn là ưu tiên tuyệt đối."
)

VI_DISCLAIMER = (
    "\n\n---\n*Thông tin này chỉ dành cho mục đích giáo dục và không phải là "
    "lời khuyên y tế. Hãy luôn tham khảo ý kiến bác sĩ nhi khoa hoặc chuyên gia "
    "y tế có chuyên môn về bất kỳ mối quan tâm nào liên quan đến sức khỏe của con bạn.*"
)

VI_SYSTEM_PROMPT_TEMPLATE = (
    "Bạn là Trợ Lý Nuôi Dạy Con Thông Minh, một hướng dẫn nuôi dạy con dựa trên bằng chứng AI.\n\n"
    "## Bối Cảnh Phát Triển Của Trẻ\n{child_context}\n\n"
    "## Hướng Dẫn Giọng Điệu\n{register_prompt}\n\n"
    "## Kiến Thức Dựa Trên Bằng Chứng\n{rag_context}\n\n"
    "{history_context}\n\n"
    "## Hướng Dẫn Trả Lời\n"
    "- Căn cứ câu trả lời của bạn vào kiến thức dựa trên bằng chứng được cung cấp\n"
    "- Tham khảo các nguồn cụ thể với nhãn mức độ bằng chứng (RCT, hướng dẫn, v.v.)\n"
    "- Hiệu chỉnh mọi lời khuyên theo độ tuổi và giai đoạn phát triển cụ thể của trẻ\n"
    "- Nếu bằng chứng không đầy đủ, hãy thừa nhận giới hạn của nghiên cứu hiện tại\n"
    "- Trả lời bằng tiếng Việt tự nhiên, phù hợp với bối cảnh gia đình Việt Nam"
)

VI_CHILD_CONTEXT_FORMAT = (
    "Trẻ: {name}, Tuổi: {age_months} tháng, "
    "Giai đoạn: {stage_vi}, Giới tính: {sex}\n"
    "Giai đoạn Erikson: {erikson_vi}\n"
    "Giai đoạn Piaget: {piaget_vi}\n"
    "Các mốc chính: {milestones_vi}\n"
    "Hướng dẫn theo giai đoạn: {guidance_vi}"
)


def get_vietnamese_developmental_context(dev_ctx: dict) -> str:
    stage = AgeStage(dev_ctx["stage"])
    return VI_CHILD_CONTEXT_FORMAT.format(
        name=dev_ctx.get("name", "Bé"),
        age_months=dev_ctx["age_months"],
        stage_vi=VI_STAGE_LABELS.get(stage, dev_ctx["stage"]),
        sex="Nữ" if dev_ctx.get("sex") == "female" else "Nam",
        erikson_vi=VI_ERIKSON_STAGE.get(stage, dev_ctx["erikson_stage"]),
        piaget_vi=VI_PIAGET_STAGE.get(stage, dev_ctx["piaget_stage"]),
        milestones_vi=", ".join(VI_MILESTONES.get(stage, [])),
        guidance_vi=VI_STAGE_GUIDANCE.get(stage, dev_ctx["stage_guidance"]),
    )


def get_vi_register_prompt(register: str) -> str:
    prompts = {
        "warm_reassuring": (
            "Tin nhắn của phụ huynh thể hiện sự lo lắng hoặc căng thẳng. "
            "Trình bày câu trả lời của bạn với sự ấm áp, đồng cảm và trấn an "
            "trong khi cung cấp thông tin chính xác dựa trên bằng chứng."
        ),
        "celebratory": (
            "Phụ huynh có vẻ tích cực và gắn kết. "
            "Đáp lại bằng sự ấm áp và khích lệ trong khi cung cấp thông tin dựa trên bằng chứng."
        ),
        "calm_informational": (
            "Phụ huynh đang hỏi một câu hỏi thông tin. "
            "Cung cấp thông tin rõ ràng, bình tĩnh, dựa trên bằng chứng "
            "mà không có khung cảm xúc không cần thiết."
        ),
    }
    return prompts.get(register, "Cung cấp hướng dẫn nuôi dạy con dựa trên bằng chứng.")
