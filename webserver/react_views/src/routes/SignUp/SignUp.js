import { useRef, forwardRef, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { Content, FlexboxGrid, Panel, Form, ButtonToolbar, Button, Schema } from 'rsuite';
import { Container, Navbar } from "react-bootstrap";
import axios from "axios";

import 'bootstrap/dist/css/bootstrap.css';
//import "./SignUp.css";

const { StringType } = Schema.Types;

const model = Schema.Model({
  name: StringType().isRequired('This field is required.'),
  email: StringType()
    // .isEmail('Please enter a valid email address.')
    .isRequired('This field is required.'),
  password: StringType().isRequired('This field is required.'),
  confirmPassword: StringType().isRequired('This field is required.'),
});

const TextField = forwardRef((props, ref) => {
  const { name, label, accepter, ...rest } = props;
  return (
    <Form.Group controlId={name} ref={ref}>
      <Form.ControlLabel>{label} </Form.ControlLabel>
      <Form.Control name={name} accepter={accepter} {...rest} />
    </Form.Group>
  );
});

const SignUp = ({setUser, setUserId, userId}) => {
  const navigate = useNavigate();
  const formRef = useRef();
  const [formValue, setFormValue] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const authenticateUser = () => {
    if(formValue.password !== formValue.confirmPassword){
	    return
    }
    const data = new FormData()
    data.append("name", formValue.name);
    data.append("email", formValue.email);
    data.append("password", formValue.password);

    axios
      .post("http://localhost:5001/api/signup_user", data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then(function (response) {
	console.log(response.data.user)
	alert(response.data.message)
        const rawUser = response.data.user 
        if (rawUser !== null && rawUser !== undefined){
		const user = { ...response.data.user, isAuth: true , files: {}}
		//setUserId(user.id);
		setUser(user);
		//localStorage.setItem('userId', user.id);
		localStorage.setItem('user', JSON.stringify(user));
		navigate("/");
	}
        else console.log("User not authenticated");

      })
      .catch(function () {
        console.log("User does not exist");
      });
  }

  return (
    <div>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand >Cardamom Workbench</Navbar.Brand>
        </Container>
      </Navbar>
      <Content className="login-form">
        <FlexboxGrid justify="center">
          <FlexboxGrid.Item colspan={12}>
            <Panel header={<h3>Sign Up</h3>} bordered>
              <Form onSubmit={authenticateUser} ref={formRef} onChange={setFormValue} formValue={formValue} model={model}>
                <TextField name="name" label="Name" />
                <TextField name="email" label="Email Address" />
                <TextField name="password" label="Password" type="password" autoComplete="off" />
                <TextField name="confirmPassword" label="Confirm Password" type="password" autoComplete="off" />
                <Form.Group>
                  <ButtonToolbar>
                    <Button appearance="primary" type="submit">Register</Button>
                  </ButtonToolbar>
                </Form.Group>
              </Form>
            </Panel>
          </FlexboxGrid.Item>
        </FlexboxGrid>
      </Content>
    </div>
  );
};
export default SignUp;
