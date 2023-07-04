<template>
    <div class="mt-5 pt-5 text-center text-danger font-weight-bold">
        <b-container fluid="md" class="mt-5">
            <b-alert show variant="danger">
                <h4 class="alert-heading">Oh snap! You got an error! Youre not Authenticated</h4>
                <p>Login to continue</p>
                <hr />
                <b-button class="mt-5" variant="outline" size="lg" block>
                    <b-link to="/">Login</b-link>
                </b-button>
            </b-alert>
        </b-container>
    </div>
</template>

<script>
export default {};
</script>

<style></style>
