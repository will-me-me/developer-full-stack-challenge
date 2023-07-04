<template>
    <b-container class="">
        <b-alert
            :show="dismissCountDown"
            dismissible
            variant="primary"
            @dismissed="dismissCountDown = 0"
            @dismiss-count-down="countDownChanged"
            class="mt-5 mb-2"
            aling="center"
        >
            <p>{{ message }} {{ dismissCountDown }}</p>
            <b-progress variant="primary" :max="dismissSecs" :value="dismissCountDown" height="2px"></b-progress>
        </b-alert>
        <b-card
            bg-variant="light"
            header="Sign In"
            border-variant="secondary"
            align=""
            class="mx-auto text-center logincard"
        >
            <b-card-body>
                <b-form @submit.prevent="onSubmit">
                    <b-form-group id="input-group-1" label="" label-for="input-1">
                        <b-form-input
                            id="input-1"
                            v-model="username"
                            type="username"
                            required
                            placeholder="Enter username"
                            :rules="usernameRules"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group
                        id="input-group-2"
                        label=" "
                        label-for="input-2"
                        :state="PasswordState"
                        :invalid-feedback="PasswordState ? '' : 'password length must be greater than 5'"
                    >
                        <b-form-input
                            id="input-2"
                            v-model="password"
                            type="password"
                            required
                            placeholder="Enter password"
                            :rules="passwordRules"
                            oninput="this.value = this.value.replace(/[^A-Za-z0-9]/g,'')"
                        >
                        </b-form-input>
                    </b-form-group>

                    <b-button :disabled="disabledLogin" pill type="submit" block variant="outline-primary"
                        >Login</b-button
                    >
                </b-form>
            </b-card-body>
        </b-card>
    </b-container>
</template>

<script>
// import { LoginUser } from '../axioscall/main.js';
import axios from 'axios';

export default {
    data() {
        return {
            dismissSecs: 1.5,
            dismissCountDown: 0,
            showDismissibleAlert: false,
            message: '',
            email: '',
            password: '',
            emailRules: [(v) => !!v || 'Email is required', (v) => /.+@.+\..+/.test(v) || 'Email must be valid'],
            passwordRules: [(v) => !!v || 'Password is required'],
            username: '',
            usernameRules: [(v) => !!v || 'Username is required'],
            passwordFieldType: 'password',
            user: {
                username: '',
                password: '',
            },
        };
    },
    computed: {
        disabledLogin() {
            return this.username === '' || this.password === '';
        },

        EmailState() {
            if (this.email === '') return null;
            return this.email.match(/.+@.+\..+/) !== null;
        },

        PasswordState() {
            if (this.password === '') return null;
            return this.password.length > 5;
        },
    },

    methods: {
        countDownChanged(dismissCountDown) {
            this.dismissCountDown = dismissCountDown;
        },
        showAlert() {
            this.dismissCountDown = this.dismissSecs;
        },
        togglePasswordVisibility() {
            this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
        },

        async userLogin() {
            const user = {
                username: this.username,
                password: this.password,
            };
            try {
                const response = await axios.post('http://127.0.0.1:8000/users/login', user);
                if (response.status === 200 && response.statusText === 'OK') {
                    //open alert
                    this.message = 'Login Successful';
                    this.showAlert();
                    //save token
                    const token = response.data.token;
                    localStorage.setItem('token', token);
                    //redirect to dashboard
                    setTimeout(() => {
                        this.$router.push('/authors');
                    }, 2000);
                }
            } catch (error) {
                if (error.response.status === 404) {
                    this.message = 'Login Failed - User not found or password incorrect';
                    this.showAlert();
                } else {
                    this.message = 'Login Failed - User not found or password incorrect';
                    this.showAlert();
                }
            }
        },

        onSubmit(evt) {
            evt.preventDefault();
            // alert(JSON.stringify(this.user));
            this.userLogin();
        },
    },
};
</script>

<style scoped>
.logincard {
    border-radius: 5px;
    max-width: 650px;
}
.input-group-append {
    cursor: pointer;
}
</style>
>
