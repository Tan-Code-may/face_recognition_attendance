import React, { useState } from 'react';
import './styles.css';
import { Link } from 'react-router-dom';

const loginInputs = [
    {
        label: "User ID",
        type: "text",
        show: true,
        validated: "",
        id: "a"
    }, {
        label: "Password",
        type: "password",
        show: true,
        validated: "",
        id: "b"
    }
];

const LoginWrapper = () => {
    const [signUp, setSignUp] = useState(false);
    const [loginInputsState, setLoginInputsState] = useState(loginInputs);
    const [userType, setUserType] = useState("student");

    const inUpClick = () => {
        setSignUp(!signUp);
        animateFields("loginInputs");
    };

    const animateFields = (formName) => {
        let newForm = loginInputsState.slice();
        let stagger = (i) => {
            if (i < newForm.length) {
                setTimeout(() => {
                    newForm[i].show = !newForm[i].show;
                    setLoginInputsState(newForm);
                    stagger(i + 1);
                }, 70);
            }
        };
        stagger(0);
    };

    const submitForm = (e) => {
        e.preventDefault();
        console.log("User Type:", userType);
    };

    const validateField = (event, id) => {
        let newState = loginInputsState.slice();
        const fieldInState = newState.find(field => field.id === id);
        fieldInState.validated = event.target.value.length > 0 ? true : false;
        setLoginInputsState(newState);
    };

    return (
        <div>
            <Login
                signUp={signUp}
                inputs={loginInputsState}
                inUpClick={inUpClick}
                submitForm={submitForm}
                validateField={validateField}
                userType={userType}
                setUserType={setUserType}
            />
        </div>
    );
};

const Login = ({ inputs, signUp, inUpClick, submitForm, validateField, userType, setUserType }) => (
    <div className={signUp ? "login login-closed" : "login"}>
        <h1>Log In</h1>
        <hr />
        <Form
            inputs={inputs}
            submitForm={submitForm}
            validateField={validateField}
            userType={userType}
            setUserType={setUserType}
        />
        <SignupLink inUpClick={inUpClick} />
    </div>
);

const Form = ({ inputs, submitForm, validateField, userType, setUserType }) => (
    <form onSubmit={submitForm}>
        {inputs.map((input) => (
            <Input
                key={input.id}
                label={input.label}
                type={input.type}
                show={input.show}
                validated={input.validated}
                id={input.id}
                validateField={validateField}
            />
        ))}
        <div className="radio-group">
            <label className="radio-label">
                <input
                    className="radio-input"
                    type="radio"
                    name="userType"
                    value="student"
                    checked={userType === "student"}
                    onChange={() => setUserType("student")}
                />
                Student
            </label>
            <label className="radio-label">
                <input
                    className="radio-input"
                    type="radio"
                    name="userType"
                    value="professor"
                    checked={userType === "professor"}
                    onChange={() => setUserType("professor")}
                />
                Professor
            </label>
        </div>
        <Submit />
    </form>
);

const Submit = () => (
    <div>
        <hr />
        <button className="submit-button" type="submit">Submit</button>
    </div>
);

const Input = ({ label, type, show, validated, id, validateField }) => (
    <div className={show ? "field field-in" : "field"}>
        <label className="label">{label}
            <i className={validated ? "fa fa-check animate-check" : ""} aria-hidden="true"></i>
        </label>
        <br />
        <input
            className="input"
            type={type}
            onBlur={(event) => validateField(event, id)}
        />
    </div>
);

const SignupLink = () => (
    <div className="signup-link">
        <p className="in-out">
            Don't have an account? {" "}
            <Link to="/register">Sign Up Here</Link>
        </p>
    </div>
);

export default LoginWrapper;