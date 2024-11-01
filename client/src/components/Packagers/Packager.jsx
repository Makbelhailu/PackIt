import React, { useState } from "react";
import axios from "axios";
import usePackageStore from "./store";
import "./Packager.css";
import defaultImage from "./default.jpg";
import { FaTrashCan } from "react-icons/fa6";

const Packager = () => {
  const [category, setCategory] = useState("All");
  const [priorityItems, setPriorityItems] = useState([]);
  const [style, setStyle] = useState("");
  const [material, setMaterial] = useState([]);
  const [colorPalette, setColorPalette] = useState([]);
  const [quality, setQuality] = useState("Standard");
  const [budget, setBudget] = useState("");

  const itemsList = [
    "Sofa",
    "Queen Bed Frame",
    "Office Desk",
    "Dining Table",
    "Washing Machine",
    "Microwave Oven",
    "Television",
    "Armchair",
    "Nightstand",
    "Refrigerator",
  ];

  const handleCheckboxChange = (e, setter, state) => {
    const { value, checked } = e.target;
    if (checked) setter([...state, value]);
    else setter(state.filter((item) => item !== value));
  };

  const { setPackageData, setShowPopup, deleteItem } = usePackageStore();

  const handleGeneratePackage = async (e) => {
    e.preventDefault();
    const requestData = {
      budget: parseInt(budget),
      essential_items: priorityItems,
      preferences: {
        style,
        material,
        color_palette: colorPalette,
        quality,
      },
    };

    try {
      const response = await axios.post(
        "http://localhost:8000/api/generate-package",
        requestData
      );
      setPackageData(response.data);
      setShowPopup(true);
    } catch (error) {
      console.error("Error generating package:", error);
    }
  };

  const handleDelete = (packageIndex, itemId) => {
    // const deleteItem = usePackageStore((state) => state.deleteItem);

    console.log(packageIndex, itemId);
    try {
      deleteItem(packageIndex, itemId);
    } catch (error) {
      console.error("Error deleting item:", error);
    }
  };

  return (
    <div className="Kcontainer">
      <h1 className="Kheader">Package</h1>
      <div className="Kgrid-container">
        <div className="Kgrid-item">
          <label>Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="All">All</option>
            <option value="Living Room">Living Room</option>
            <option value="Bedroom">Bedroom</option>
            <option value="Kitchen">Kitchen</option>
          </select>
        </div>
        <div className="Kgrid-item">
          <label>Your Priority Items</label>
          {itemsList.map((item, index) => (
            <div key={index}>
              <input
                type="checkbox"
                value={item}
                onChange={(e) =>
                  handleCheckboxChange(e, setPriorityItems, priorityItems)
                }
              />
              {item}
            </div>
          ))}
        </div>
        <div className="Kgrid-item">
          <label>Style</label>
          <select value={style} onChange={(e) => setStyle(e.target.value)}>
            <option value="">Select Style</option>
            <option value="Modern">Modern</option>
            <option value="Traditional">Traditional</option>
            <option value="Normal">Normal</option>
          </select>
        </div>
        <div className="Kgrid-item">
          <label>Material</label>
          {["Wood", "Metal", "Fabric"].map((materialOption, index) => (
            <div key={index}>
              <input
                type="checkbox"
                value={materialOption}
                onChange={(e) => handleCheckboxChange(e, setMaterial, material)}
              />
              {materialOption}
            </div>
          ))}
        </div>
        <div className="Kgrid-item">
          <label>Color Palette</label>
          {["Neutral", "Dark", "White"].map((color, index) => (
            <div key={index}>
              <input
                type="checkbox"
                value={color}
                onChange={(e) =>
                  handleCheckboxChange(e, setColorPalette, colorPalette)
                }
              />
              {color}
            </div>
          ))}
        </div>
        <div className="Kgrid-item">
          <label>Quality</label>
          <select value={quality} onChange={(e) => setQuality(e.target.value)}>
            <option value="">Select Quality</option>
            <option value="Premium">Premium</option>
            <option value="Luxury">Luxury</option>
            <option value="Standard">Standard</option>
          </select>
        </div>
        <div className="Kgrid-item">
          <label>Budget</label>
          <input
            type="text"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            placeholder="Enter Budget"
          />
        </div>
      </div>
      <button className="Kgenerate-button" onClick={handleGeneratePackage}>
        PackIt
      </button>
      <PackagePopup handleDelete={handleDelete} budget={budget} />
    </div>
  );
};

// Popup component to show generated packages with inline Product Card
const PackagePopup = ({ handleDelete, budget }) => {
  const { packageData, showPopup, setShowPopup } = usePackageStore();

  if (!showPopup || !packageData) return null;

  return (
    <div className="Kpopup">
      <div className="Kpopup-content">
        <button
          className="Kclose-top-button"
          onClick={() => setShowPopup(false)}
        >
          &times;
        </button>
        <h2 style={{ fontSize: "1.5rem", fontWeight: 600 }}>
          Generated Packages
        </h2>
        {packageData.packages.map((pkg, pIndex) => (
          <div
            key={pIndex}
            className="Kpackage"
            style={{ marginBottom: "2rem", padding: "1rem" }}
          >
            <h3
              style={{
                fontSize: "1.25rem",
                fontWeight: 600,
                marginBottom: "1.5rem",
              }}
            >
              Package {pIndex + 1}
            </h3>
            <div className="Kproduct-list">
              {pkg.items.map((item, index) => (
                <div key={index} className="Kproduct-card">
                  <img
                    src={item.img ? item.img : defaultImage}
                    alt={item.name}
                    className="Kproduct-image"
                  />

                  <h4 className="Kproduct-name">{item.name}</h4>
                  <p className="Kproduct-style">Style: {item.style}</p>
                  <p className="Kproduct-price">${item.price}</p>
                  <div className="trashcan-icon">
                    <FaTrashCan
                      onClick={() => handleDelete(pIndex, item.id, budget)}
                    />
                  </div>
                </div>
              ))}
            </div>
            <div style={{ fontSize: "1.125rem", marginTop: "1.5rem" }}>
              <p>Total Price: ${pkg.total_price}</p>
              <p>Remaining Budget: ${pkg.remaining_budget}</p>
              <p>Similarity Score: {pkg.similarity_score}%</p>
            </div>
            <button className="Kadd-to-cart">Add Package</button>
          </div>
        ))}
        <button onClick={() => setShowPopup(false)}>Close</button>
      </div>
    </div>
  );
};

export default Packager;
