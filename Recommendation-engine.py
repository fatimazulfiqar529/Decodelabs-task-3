import sys
import math
from collections import Counter
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QScrollArea, QFrame,
    QGridLayout, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPalette

JOB_ROLES = {
    "Data Scientist": ["python","machine learning","sql","statistics","data analysis","tensorflow","pandas","numpy","deep learning","data visualization"],
    "ML Engineer": ["python","machine learning","tensorflow","pytorch","deep learning","algorithms","model deployment","docker","numpy","scikit-learn"],
    "Backend Developer": ["python","java","sql","apis","node.js","databases","rest api","docker","microservices","git"],
    "Frontend Developer": ["javascript","html","css","react","vue","ui design","web design","typescript","responsive design","git"],
    "Full Stack Developer": ["javascript","python","html","css","react","sql","node.js","git","apis","databases"],
    "DevOps Engineer": ["docker","kubernetes","aws","cloud","ci/cd","linux","automation","git","terraform","monitoring"],
    "Cloud Architect": ["aws","cloud","azure","kubernetes","docker","networking","security","automation","terraform","microservices"],
    "Cybersecurity Analyst": ["networking","security","linux","penetration testing","encryption","firewalls","python","ethical hacking","risk assessment","siem"],
    "AI Engineer": ["python","machine learning","deep learning","nlp","tensorflow","pytorch","algorithms","data analysis","model deployment","cloud"],
    "Data Analyst": ["sql","excel","python","data visualization","statistics","tableau","power bi","data analysis","reporting","pandas"],
    "Mobile Developer": ["java","kotlin","swift","flutter","react native","android","ios","apis","ui design","git"],
    "Database Administrator": ["sql","databases","oracle","mysql","postgresql","backup","performance tuning","linux","security","data modeling"],
    "System Administrator": ["linux","windows server","networking","automation","security","cloud","virtualization","monitoring","bash","powershell"],
    "Blockchain Developer": ["solidity","ethereum","smart contracts","python","javascript","cryptography","web3","decentralized","git","security"],
    "Game Developer": ["c++","unity","unreal engine","game design","python","graphics","physics simulation","3d modeling","git","algorithms"],
}

SUGGESTED_SKILLS = [
    "Python","SQL","Machine Learning","Docker","AWS",
    "JavaScript","React","Cloud","Linux","TensorFlow",
    "Java","Security","Data Analysis","Kubernetes","Node.js",
    "Deep Learning","Algorithms","Automation","Git","Statistics",
    "Networking","NLP","PyTorch","Flutter","TypeScript",
]

ROLE_ICONS = {
    "Data Scientist": "🔬", "ML Engineer": "🤖", "Backend Developer": "⚙️",
    "Frontend Developer": "🎨", "Full Stack Developer": "🧩", "DevOps Engineer": "🚀",
    "Cloud Architect": "☁️", "Cybersecurity Analyst": "🛡️", "AI Engineer": "🧠",
    "Data Analyst": "📊", "Mobile Developer": "📱", "Database Administrator": "🗄️",
    "System Administrator": "🖥️", "Blockchain Developer": "🔗", "Game Developer": "🎮",
}

def build_vocabulary(job_roles):
    vocab = set()
    for skills in job_roles.values():
        vocab.update(skills)
    return sorted(list(vocab))

def compute_tf(skill_list):
    count = Counter(skill_list)
    total = len(skill_list)
    return {skill: count[skill] / total for skill in count}

def compute_idf(job_roles):
    total_roles = len(job_roles)
    skill_doc_count = Counter()
    for skills in job_roles.values():
        for skill in set(skills):
            skill_doc_count[skill] += 1
    return {skill: math.log(total_roles / cnt) for skill, cnt in skill_doc_count.items()}

def compute_tfidf_vector(skill_list, vocabulary, idf):
    tf = compute_tf(skill_list)
    return [tf.get(t, 0) * idf.get(t, 0) for t in vocabulary]

def cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a ** 2 for a in vec_a))
    mag_b = math.sqrt(sum(b ** 2 for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

def recommend(user_skills_raw, top_n=3):
    user_skills = [s.strip().lower() for s in user_skills_raw]
    vocabulary = build_vocabulary(JOB_ROLES)
    idf = compute_idf(JOB_ROLES)
    user_vector = compute_tfidf_vector(user_skills, vocabulary, idf)
    scores = {}
    for role, skills in JOB_ROLES.items():
        role_vector = compute_tfidf_vector(skills, vocabulary, idf)
        scores[role] = cosine_similarity(user_vector, role_vector)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]


class SkillChip(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.selected = False
        self.setCheckable(True)
        self.setFixedHeight(34)
        self._apply_style()
        self.toggled.connect(self._on_toggle)

    def _on_toggle(self, checked):
        self.selected = checked
        self._apply_style()

    def _apply_style(self):
        if self.selected:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #6C63FF;
                    color: white;
                    border: 2px solid #6C63FF;
                    border-radius: 17px;
                    padding: 0px 16px;
                    font-size: 13px;
                    font-weight: 600;
                }
                QPushButton:hover { background-color: #5A52E0; }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2A2A3E;
                    color: #A0A0C0;
                    border: 1.5px solid #3A3A5C;
                    border-radius: 17px;
                    padding: 0px 16px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #32325A;
                    color: #CCCCFF;
                    border-color: #6C63FF;
                }
            """)


class ResultCard(QFrame):
    def __init__(self, rank, role, score, key_skills, parent=None):
        super().__init__(parent)
        self.setObjectName("resultCard")
        rank_colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
        rank_labels = ["🥇  #1 Best Match", "🥈  #2 Match", "🥉  #3 Match"]
        bar_colors  = ["#6C63FF", "#4ECDC4", "#FF6B9D"]
        pct  = score * 100
        icon = ROLE_ICONS.get(role, "💼")
        self.setStyleSheet(f"""
            QFrame#resultCard {{
                background-color: #1E1E2F;
                border: 1.5px solid {rank_colors[rank]};
                border-radius: 16px;
                padding: 8px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 18, 20, 18)
        badge = QLabel(rank_labels[rank])
        badge.setStyleSheet(f"color: {rank_colors[rank]}; font-size: 12px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(badge)
        role_row = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 28px;")
        icon_lbl.setFixedWidth(40)
        role_lbl = QLabel(role)
        role_lbl.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: 700;")
        role_row.addWidget(icon_lbl)
        role_row.addWidget(role_lbl)
        role_row.addStretch()
        pct_lbl = QLabel(f"{pct:.1f}%")
        pct_lbl.setStyleSheet(f"color: {bar_colors[rank]}; font-size: 22px; font-weight: 700;")
        role_row.addWidget(pct_lbl)
        layout.addLayout(role_row)
        bar = QProgressBar()
        bar.setValue(int(pct))
        bar.setTextVisible(False)
        bar.setFixedHeight(8)
        bar.setStyleSheet(f"""
            QProgressBar {{ background-color: #2A2A3E; border-radius: 4px; border: none; }}
            QProgressBar::chunk {{ background-color: {bar_colors[rank]}; border-radius: 4px; }}
        """)
        layout.addWidget(bar)
        skills_label = QLabel("Key Skills Required:")
        skills_label.setStyleSheet("color: #7070A0; font-size: 12px; margin-top: 4px;")
        layout.addWidget(skills_label)
        skills_row = QHBoxLayout()
        skills_row.setSpacing(6)
        for skill in key_skills[:5]:
            s = QLabel(skill.title())
            s.setStyleSheet("""
                background-color: #2A2A3E;
                color: #9090D0;
                border: 1px solid #3A3A5C;
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 11px;
            """)
            skills_row.addWidget(s)
        skills_row.addStretch()
        layout.addLayout(skills_row)


class TechStackRecommender(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_skills = set()
        self.chip_widgets = {}
        self.setWindowTitle("DecodeLabs — Tech Stack Recommender")
        self.setMinimumSize(900, 700)
        self.resize(1000, 780)
        self._setup_ui()
        self._apply_global_style()

    def _apply_global_style(self):
        self.setStyleSheet("""
            QMainWindow, QWidget#central { background-color: #12121C; }
            QScrollArea { background-color: transparent; border: none; }
            QScrollBar:vertical { background: #1A1A2E; width: 6px; border-radius: 3px; }
            QScrollBar::handle:vertical { background: #3A3A6A; border-radius: 3px; }
            QLineEdit {
                background-color: #1E1E2F;
                color: #E0E0FF;
                border: 1.5px solid #3A3A5C;
                border-radius: 20px;
                padding: 8px 18px;
                font-size: 13px;
            }
            QLineEdit:focus { border-color: #6C63FF; }
        """)

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(110)
        header.setStyleSheet("background-color: #0D0D1A; border-bottom: 1px solid #2A2A40;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(40, 0, 40, 0)
        logo = QLabel("⚡")
        logo.setStyleSheet("font-size: 32px;")
        h_layout.addWidget(logo)
        title_col = QVBoxLayout()
        title = QLabel("Tech Stack Recommender")
        title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: 700; letter-spacing: 0.5px;")
        sub = QLabel("DecodeLabs · Project 3 · TF-IDF + Cosine Similarity")
        sub.setStyleSheet("color: #6060A0; font-size: 12px;")
        title_col.addWidget(title)
        title_col.addWidget(sub)
        h_layout.addLayout(title_col)
        h_layout.addStretch()
        self.counter_lbl = QLabel("0 / 3 skills selected")
        self.counter_lbl.setStyleSheet("color: #6060A0; font-size: 13px;")
        h_layout.addWidget(self.counter_lbl)
        root.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        body_widget = QWidget()
        body_widget.setStyleSheet("background-color: #12121C;")
        body_layout = QVBoxLayout(body_widget)
        body_layout.setContentsMargins(40, 30, 40, 30)
        body_layout.setSpacing(28)
        scroll.setWidget(body_widget)
        root.addWidget(scroll)

        sec1_title = QLabel("Select Your Skills")
        sec1_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 700;")
        body_layout.addWidget(sec1_title)
        hint = QLabel("Click to select · minimum 3 required · more = better accuracy")
        hint.setStyleSheet("color: #50507A; font-size: 12px; margin-top: -10px;")
        body_layout.addWidget(hint)

        self.chip_frame = QFrame()
        self.chip_frame.setStyleSheet("background-color: #16162A; border-radius: 14px; padding: 6px;")
        self.chip_grid = QGridLayout(self.chip_frame)
        self.chip_grid.setSpacing(8)
        self.chip_grid.setContentsMargins(16, 16, 16, 16)
        cols = 6
        for idx, skill in enumerate(SUGGESTED_SKILLS):
            chip = SkillChip(skill)
            chip.toggled.connect(lambda checked, s=skill: self._on_chip_toggle(s, checked))
            self.chip_grid.addWidget(chip, idx // cols, idx % cols)
            self.chip_widgets[skill] = chip
        body_layout.addWidget(self.chip_frame)

        custom_row = QHBoxLayout()
        self.custom_input = QLineEdit()
        self.custom_input.setPlaceholderText("Add a custom skill (e.g. Solidity, Rust, Figma)...")
        self.custom_input.setFixedHeight(42)
        self.custom_input.returnPressed.connect(self._add_custom_skill)
        add_btn = QPushButton("+ Add")
        add_btn.setFixedHeight(42)
        add_btn.setFixedWidth(100)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2A2A3E;
                color: #9090D0;
                border: 1.5px solid #3A3A5C;
                border-radius: 21px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #6C63FF; color: white; border-color: #6C63FF; }
        """)
        add_btn.clicked.connect(self._add_custom_skill)
        custom_row.addWidget(self.custom_input)
        custom_row.addWidget(add_btn)
        body_layout.addLayout(custom_row)

        self.selected_frame = QFrame()
        self.selected_frame.setStyleSheet("QFrame { background-color: #16162A; border-radius: 12px; }")
        self.selected_frame.setVisible(False)
        sel_layout = QVBoxLayout(self.selected_frame)
        sel_layout.setContentsMargins(16, 14, 16, 14)
        sel_layout.setSpacing(8)
        sel_title = QLabel("Your Selected Skills:")
        sel_title.setStyleSheet("color: #7070A0; font-size: 12px; font-weight: 600;")
        sel_layout.addWidget(sel_title)
        self.selected_tags_row = QHBoxLayout()
        self.selected_tags_row.setSpacing(6)
        sel_layout.addLayout(self.selected_tags_row)
        body_layout.addWidget(self.selected_frame)

        self.run_btn = QPushButton("🔍  Find My Career Matches")
        self.run_btn.setFixedHeight(52)
        self.run_btn.setEnabled(False)
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C63FF;
                color: white;
                border: none;
                border-radius: 26px;
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            QPushButton:hover  { background-color: #5A52E0; }
            QPushButton:pressed { background-color: #4A42C0; }
            QPushButton:disabled { background-color: #2A2A3E; color: #404070; }
        """)
        self.run_btn.clicked.connect(self._run_recommender)
        body_layout.addWidget(self.run_btn)

        self.results_frame = QFrame()
        self.results_frame.setVisible(False)
        self.results_layout = QVBoxLayout(self.results_frame)
        self.results_layout.setSpacing(14)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.addWidget(self.results_frame)

        footer = QLabel("DecodeLabs · Batch 2026 · Content-Based Filtering · TF-IDF + Cosine Similarity")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #30305A; font-size: 11px; margin-top: 10px;")
        body_layout.addWidget(footer)
        body_layout.addStretch()

    def _on_chip_toggle(self, skill, checked):
        if checked:
            self.selected_skills.add(skill)
        else:
            self.selected_skills.discard(skill)
        self._refresh_ui()

    def _remove_skill(self, skill):
        self.selected_skills.discard(skill)
        if skill in self.chip_widgets:
            self.chip_widgets[skill].blockSignals(True)
            self.chip_widgets[skill].setChecked(False)
            self.chip_widgets[skill].blockSignals(False)
            self.chip_widgets[skill]._apply_style()
        self._refresh_ui()

    def _add_custom_skill(self):
        text = self.custom_input.text().strip()
        if not text:
            return
        if text not in self.chip_widgets:
            chip = SkillChip(text)
            chip.toggled.connect(lambda checked, s=text: self._on_chip_toggle(s, checked))
            count = self.chip_grid.count()
            cols = 6
            self.chip_grid.addWidget(chip, count // cols, count % cols)
            self.chip_widgets[text] = chip
            chip.setChecked(True)
        else:
            self.chip_widgets[text].setChecked(True)
        self.custom_input.clear()

    def _refresh_ui(self):
        count = len(self.selected_skills)
        self.counter_lbl.setText(f"{count} / 3 skills selected")
        if count >= 3:
            self.counter_lbl.setStyleSheet("color: #6C63FF; font-size: 13px; font-weight: 700;")
            self.run_btn.setEnabled(True)
        else:
            self.counter_lbl.setStyleSheet("color: #6060A0; font-size: 13px;")
            self.run_btn.setEnabled(False)

        while self.selected_tags_row.count():
            item = self.selected_tags_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.selected_skills:
            self.selected_frame.setVisible(True)
            for skill in sorted(self.selected_skills):
                tag_widget = QWidget()
                tag_widget.setStyleSheet("""
                    QWidget {
                        background-color: #6C63FF;
                        border-radius: 12px;
                    }
                """)
                tag_layout = QHBoxLayout(tag_widget)
                tag_layout.setContentsMargins(10, 4, 6, 4)
                tag_layout.setSpacing(4)

                skill_lbl = QLabel(f"✓ {skill}")
                skill_lbl.setStyleSheet("color: white; font-size: 12px; font-weight: 600; background: transparent;")
                tag_layout.addWidget(skill_lbl)

                remove_btn = QPushButton("✕")
                remove_btn.setFixedSize(18, 18)
                remove_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255,255,255,0.25);
                        color: white;
                        border: none;
                        border-radius: 9px;
                        font-size: 10px;
                        font-weight: 700;
                        padding: 0px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255,255,255,0.5);
                    }
                """)
                remove_btn.clicked.connect(lambda _, s=skill: self._remove_skill(s))
                tag_layout.addWidget(remove_btn)

                self.selected_tags_row.addWidget(tag_widget)
            self.selected_tags_row.addStretch()
        else:
            self.selected_frame.setVisible(False)

        self.results_frame.setVisible(False)

    def _run_recommender(self):
        if len(self.selected_skills) < 3:
            return
        self.run_btn.setText("⏳  Calculating matches...")
        self.run_btn.setEnabled(False)
        QTimer.singleShot(600, self._show_results)

    def _show_results(self):
        results = recommend(list(self.selected_skills), top_n=3)
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        res_title = QLabel("🎯  Top Career Matches For You")
        res_title.setStyleSheet("color: #FFFFFF; font-size: 17px; font-weight: 700; margin-bottom: 4px;")
        self.results_layout.addWidget(res_title)
        for rank, (role, score) in enumerate(results):
            key_skills = JOB_ROLES.get(role, [])
            card = ResultCard(rank, role, score, key_skills)
            self.results_layout.addWidget(card)
        note = QLabel("Algorithm: Content-Based Filtering  ·  TF-IDF Weighting  ·  Cosine Similarity")
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet("color: #40406A; font-size: 11px; margin-top: 8px;")
        self.results_layout.addWidget(note)
        self.results_frame.setVisible(True)
        self.run_btn.setText("🔍  Find My Career Matches")
        self.run_btn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window,          QColor("#12121C"))
    palette.setColor(QPalette.WindowText,      QColor("#E0E0FF"))
    palette.setColor(QPalette.Base,            QColor("#1E1E2F"))
    palette.setColor(QPalette.AlternateBase,   QColor("#16162A"))
    palette.setColor(QPalette.Text,            QColor("#E0E0FF"))
    palette.setColor(QPalette.ButtonText,      QColor("#E0E0FF"))
    palette.setColor(QPalette.Highlight,       QColor("#6C63FF"))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    app.setPalette(palette)
    window = TechStackRecommender()
    window.show()
    sys.exit(app.exec_())