# deadline-heatmap

An interactive visualization tool that turns Notion (or CSV-based) assignment data into a **calendar-style stress heatmap**, helping students understand workload spikes across time and courses.

---

## ✨ Features

- 📅 Calendar-style heatmap of deadlines over time  
- 📊 Weighted workload scoring (homework, labs, exams, etc.)  
- 🧠 Per-course workload breakdown (Seaborn heatmaps)  
- 🔥 Interactive Plotly dashboard with hover details  
- 🎨 Color-coded assignment types for quick scanning  
- 📌 Highlights high-stress periods automatically  

---  

## 📊 What It Shows  

This tool converts raw assignment data into:  

- Weekly workload intensity  
- Daily stress accumulation  
- Assignment clustering over time  
- Course-specific difficulty patterns  

Example insights:  
- “Exam-heavy weeks immediately visible”  
- “Assignment clustering before deadlines"  
- “Which days consistently feel overloaded”  

---

## 🧾 Input Format  

Your CSV should look like:  
name,course,date,status,type,quarter  
HW1,Course,2026-04-10,Not Done,homework,Spring  
Lab2,Course,2026-04-12,Done,lab,Spring  
Midterm,Course,2026-04-18,Not Done,exam,Spring  
 

### Required columns:  
- `name` → assignment name    
- `course` → course code  
- `date` → due date   
- `status` → Done / Not Done  
- `type` → homework / lab / exam / assignment  
- `quarter` → term filter  

---

## ⚙️ How It Works  

1. Loads CSV exported from Notion  
2. Cleans and parses dates  
3. Assigns workload weights:  
   - homework → 1  
   - assignment → 1.5  
   - lab → 2  
   - exam → 3  
4. Aggregates workload per day  
5. Builds:  
   - static Seaborn heatmaps (per course)  
   - interactive Plotly calendar heatmap  

---  

## 📦 Dependencies  

```bash  
pip install pandas seaborn matplotlib plotly  
```  

## Run  
python heatmap.py  

