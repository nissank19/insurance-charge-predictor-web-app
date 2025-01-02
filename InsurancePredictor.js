import React, { useState } from "react";
import "./InsurancePredictor.css";

const InsurancePredictor = () => {
  const [formData, setFormData] = useState({
    age: "",
    sex: "male",
    bmi: "",
    children: "",
    smoker: "no",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (response.ok) {
        setResult(`Predicted Charges: $${data.prediction}`);
      } else {
        alert(`An error occurred: ${data.error}`);
      }
    } catch (error) {
      alert(`An error occurred: ${error.message}`);
    }
  };

  return (
    <div className="predictor-container">
      <h1>Insurance Charges Predictor</h1>
      <form onSubmit={handleSubmit}>
        <label>Age:</label>
        <input
          type="number"
          name="age"
          value={formData.age}
          onChange={handleChange}
          required
        />
        <label>Sex:</label>
        <select name="sex" value={formData.sex} onChange={handleChange}>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
        <label>BMI:</label>
        <input
          type="number"
          name="bmi"
          value={formData.bmi}
          onChange={handleChange}
          step="0.1"
          required
        />
        <label>Children:</label>
        <input
          type="number"
          name="children"
          value={formData.children}
          onChange={handleChange}
          required
        />
        <label>Smoker:</label>
        <select name="smoker" value={formData.smoker} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
        <button type="submit">Predict</button>
      </form>
      {result && <p>{result}</p>}
    </div>
  );
};

export default InsurancePredictor;
