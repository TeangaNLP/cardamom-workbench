import { useRef, forwardRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Button,
  TextField,
  Box,
  Typography,
  Snackbar,
  SnackbarContent,
  Alert,
} from "@mui/material";
import { Container, Navbar } from "react-bootstrap";
import axios from "axios";

import "./Login.css";

const Login = ({ setUser, setUserId, userId }) => {
  const navigate = useNavigate();
  const formRef = useRef();
  const [statusMessage, setStatusMessage] = useState("");
  const [formValue, setFormValue] = useState({
    email: "",
    password: "",
  });
  const [saveSuccess, setSaveSuccess] = useState(false); // New state for save success
  const [errorSuccess, setErrorSuccess] = useState(false); // New state for save success

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormValue((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const authenticateUser = (event) => {
    event.preventDefault();
    if (!formValue.email || !formValue.password) {
      return;
    }

    const data = new FormData();
    data.append("email", formValue.email);
    data.append("password", formValue.password);
    const login_user_url = process.env.REACT_APP_PORT
      ? `http://${process.env.REACT_APP_HOST}:${process.env.REACT_APP_PORT}/api/login_user`
      : `https://${process.env.REACT_APP_HOST}/api/login_user`;
    axios
      .post(login_user_url, data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(async (response) => {
        const rawUser = response.data.user;
        if (rawUser) {
          console.log("GOOD");

          setSaveSuccess(true);

          setTimeout(() => {
            const user = { ...response.data.user, isAuth: true, documents: {} };
            setUser(user);
            localStorage.setItem("user", JSON.stringify(user));
            setSaveSuccess(false);
            navigate("/files");
          }, 1200);
        } else {
          console.log("response.data.message", response.data.message);
          // setStatusMessage(response.data.message);
          setSaveSuccess(false);
          setErrorSuccess(true);

          setTimeout(() => {
            setErrorSuccess(false);
          }, 3000);
        }
      })
      .catch(function (response) {
        setErrorSuccess(true);
        setTimeout(() => {
          setErrorSuccess(false);
        }, 3000);
        console.log(response);
        // setStatusMessage(response.data.message);
        console.log("User does not exist");
      });
  };

  return (
    <div className="main-div">
      <div className="box-container">
        <div className="register">
          <div className="container left-box">
            <img
              className="screenshot-img"
              src="./cardamom-screenshot.png"
              alt="Cardamom Screenshot"
            />
            <Typography className="typo-text" variant="h4">
              Comparative deep models for minority and historical languages
            </Typography>
          </div>
        </div>
        <div className="login">
          <img
            className="cardamom-logo"
            src="./cardamom-transparent.png"
            alt="Cardamom Logo"
          />
          <div className="box-container loginbox">
            <Typography variant="h3">Log in</Typography>
            <form ref={formRef} onSubmit={authenticateUser}>
              <TextField
                fullWidth
                margin="normal"
                label="Email Address"
                name="email"
                value={formValue.email}
                onChange={handleChange}
                required
              />
              <TextField
                fullWidth
                margin="normal"
                label="Password"
                name="password"
                type="password"
                value={formValue.password}
                onChange={handleChange}
                autoComplete="off"
                required
              />
              {statusMessage && (
                <Typography color="error">{statusMessage}</Typography>
              )}
              <Box mt={2}>
                <Button variant="contained" color="primary" type="submit">
                  Login
                </Button>
                <div className="signup-div">
                  Don't have an account yet?{"   "}
                  <a
                    className="signup-link"
                    onClick={() => navigate("/signup")}
                  >
                    &nbsp;Create Here
                  </a>
                </div>
              </Box>
            </form>
          </div>
        </div>
      </div>
      <Snackbar
        open={saveSuccess}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        // autoHideDuration={}
      >
        <Alert
          severity="success"
          color="info"
          variant="filled"
          sx={{
            width: "100%",
            color: "#389e0d",
            background: "#f6ffed",
            borderColor: "#b7eb8f",
          }}
        >
          Logged In Successfully!
        </Alert>
      </Snackbar>
      <Snackbar
        open={errorSuccess}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        autoHideDuration={3000}
      >
        <Alert
          severity="error"
          sx={{
            width: "100%",
            color: "#d4380d",
            background: "#fff2e8",
            borderColor: "#ffbb96",
          }}
          variant="filled"
        >
          Error! Invalid User or Password
        </Alert>
      </Snackbar>
    </div>
  );
};

export default Login;
