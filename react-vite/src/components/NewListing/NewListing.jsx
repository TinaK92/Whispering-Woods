import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  fetchCreateListing,
  fetchDeleteListing,
  fetchUpdateListing,
} from "../../redux/listing";
import "./NewListing.css"

export const NewListing = () => {
    const dispatch = useDispatch();
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [basePrice, setBasePrice] = useState("");
    const [image, setImage] = useState(null)
  return (
    <div>
      <h1>Create New Listing</h1>
      <form></form>
    </div>
  );
};

export default NewListing;
