import { createBrowserRouter } from "react-router-dom";
import LoginFormPage from "../components/LoginFormPage";
import SignupFormPage from "../components/SignupFormPage";
import Layout from "./Layout";
import { HomePage } from "../components/HomePage/HomePage";
import Listings from "../components/Listings/Listings";
import NewListing from "../components/NewListing/NewListing";
import EditListing from "../components/EditListing/EditListing";
import ListingDetails from "../components/ListingDetails/ListingDetails";

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "login",
        element: <LoginFormPage />,
      },
      {
        path: "signup",
        element: <SignupFormPage />,
      },
      {
        path: "listings",
        element: <Listings />,
      },
      {
        path: "listings/new",
        element: <NewListing />,
      },
      {
        path: "listings/:id",
        element: <ListingDetails />,
      },
      {
        path: "listings/:id/edit",
        element: <EditListing />,
      },
    ],
  },
]);
