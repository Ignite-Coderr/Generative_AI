import { api } from "../api/api";

export default function ResumeUpload() {
  const handleUpload = async (e) => {
    const formData = new FormData();
    formData.append("resume", e.target.files[0]);

    const res = await api.post("/resume/upload", formData);
    alert("Resume uploaded. Resume ID: " + res.data.resume_id);
  };

  return <input type="file" accept=".pdf" onChange={handleUpload} />;
}
