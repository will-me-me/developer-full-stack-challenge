<template>
    <div>
        <b-container style="margin-top: 180px !important">
            <b-row>
                <b-col>
                    <b-card class="mb-2">
                        <template>
                            <b-button pill variant="outline-primary" class="mb-2 mr-2" @click="addAuthorModal"
                                >Add Author</b-button
                            >
                            <b-form-input v-model="searchQuery" placeholder="Search" class="mb-2"></b-form-input>
                        </template>
                        <b-card-text>
                            <b-table
                                striped
                                hover
                                :items="filteredAuthors"
                                :fields="fields"
                                responsive="sm"
                                class="mt-3 mb-3 text-justify text-muted"
                                @row-clicked="openmodal"
                                :current-page="currentPage"
                                :per-page="perPage"
                            ></b-table>
                            <b-pagination
                                v-model="currentPage"
                                :total-rows="filteredAuthors.length"
                                :per-page="perPage"
                                align="center"
                                class="mt-3"
                                aria-controls="my-table"
                            ></b-pagination>
                        </b-card-text>
                    </b-card>
                </b-col>
            </b-row>
        </b-container>
        <!-- add author modal -->
        <b-modal id="addauthor" title="Add Author" size="lg" hide-footer v-model="addauthormodal" centered>
            <b-container>
                <b-row>
                    <b-col>
                        <!-- @submit.prevent="onSubmit" @reset="onReset" v-if="show" -->
                        <b-form @submit.prevent="onSubmit">
                            <b-form-group id="input-group-1" label="Name:" label-for="input-1">
                                <b-form-input
                                    id="input-1"
                                    v-model="name"
                                    type="text"
                                    placeholder="Enter name"
                                    required
                                ></b-form-input>
                            </b-form-group>
                            <div class="d-flex justify-content-between">
                                <b-button pill type="submit" variant="primary">Submit</b-button>
                                <b-button pill type="reset" variant="warning" @click="CloseAddModal">Cancel</b-button>
                            </div>
                        </b-form>
                    </b-col>
                </b-row>
            </b-container>
        </b-modal>
        <!-- edit author modal -->
        <b-modal id="editauthor" title="Edit Author" size="lg" hide-footer v-model="editauthormodal" centered>
            <b-container>
                <b-row>
                    <b-col>
                        <!-- @submit.prevent="onSubmit" @reset="onReset" v-if="show" -->
                        <b-form>
                            <b-form-group id="input-group-1" label="Name:" label-for="input-1">
                                <b-form-input
                                    id="input-1"
                                    v-model="selectedAuthor.name"
                                    type="text"
                                    placeholder="Enter name"
                                    required
                                ></b-form-input>
                            </b-form-group>
                            <b-table
                                striped
                                hover
                                :items="books"
                                :fields="bookFields"
                                responsive="sm"
                                class="mt-3 mb-3 text-justify text-muted"
                                @row-clicked="OpenUpdatedbooksmodal"
                                :current-page="AuthorbookcurrentPage"
                                :per-page="authorbooksperPage"
                            ></b-table>
                            <b-pagination
                                v-model="AuthorbookcurrentPage"
                                :total-rows="books.length"
                                :per-page="authorbooksperPage"
                                align="center"
                                class="mt-3"
                                aria-controls="my-table"
                            ></b-pagination>
                            <div class="d-flex justify-content-between">
                                <b-button pill variant="primary" @click="openaddbookmodal">Addbook</b-button>

                                <b-button pill type="reset" variant="warning" @click="CloseEditModal">Cancel</b-button>
                                <!-- <b-button pill type="reset" variant="danger" @click="CloseEditModal">Delete</b-button> -->
                            </div>
                        </b-form>
                    </b-col>
                </b-row>
            </b-container>
        </b-modal>

        <!-- end edit author modal -->

        <!-- moadel to add a book -->
        <b-modal id="addbook" title="Add Book" size="lg" hide-footer v-model="Addbooksmodal" centered>
            <b-container>
                <b-row>
                    <b-col>
                        <!-- @submit.prevent="onSubmit" @reset="onReset" v-if="show" -->
                        <b-form @submit.prevent="onSubnitForAuthor">
                            <b-form-group id="input-group-1" label="Title:" label-for="input-1">
                                <b-form-input
                                    id="input-1"
                                    v-model="title"
                                    type="text"
                                    placeholder="Book title"
                                    required
                                ></b-form-input>
                            </b-form-group>
                            <b-form-group id="input-group-3" label="Pages:" label-for="input-3">
                                <b-form-input
                                    id="input-3"
                                    v-model="pages"
                                    type="number"
                                    placeholder="Number of Pages"
                                    required
                                ></b-form-input>
                            </b-form-group>
                            <div class="d-flex justify-content-between">
                                <b-button pill type="submit" variant="primary">Submit</b-button>
                                <b-button pill type="reset" variant="warning" @click="closeAddbookModals"
                                    >Cancel</b-button
                                >
                            </div>
                        </b-form>
                    </b-col>
                </b-row>
            </b-container>
        </b-modal>
        <!-- end model to add a book -->

        <!-- modal to edit a book -->
        <b-modal id="addbook" title="Update Book" size="lg" hide-footer v-model="Updatedbooksmodal" centered>
            <b-container>
                <b-row>
                    <b-col>
                        <!-- @submit.prevent="onSubmit" @reset="onReset" v-if="show" -->
                        <b-form @submit.prevent="onSubmitUpdate">
                            <b-form-group id="input-group-1" label="Title:" label-for="input-1">
                                <b-form-input
                                    id="input-1"
                                    v-model="selectedBook.name"
                                    type="text"
                                    placeholder="Book title"
                                    required
                                ></b-form-input>
                            </b-form-group>

                            <b-form-group id="input-group-3" label="Pages:" label-for="input-3">
                                <b-form-input
                                    id="input-3"
                                    v-model="selectedBook.page_numbers"
                                    type="number"
                                    placeholder="Number of Pages"
                                    required
                                ></b-form-input>
                            </b-form-group>
                            <div class="d-flex justify-content-between">
                                <b-button pill type="submit" variant="primary">Update</b-button>
                                <b-button pill type="reset" variant="danger" @click="deleteAuthorById">Delete</b-button>
                            </div>
                        </b-form>
                    </b-col>
                </b-row>
            </b-container>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios';
// import { add } from 'lodash';

export default {
    middleware: 'auth',
    data() {
        return {
            searchQuery: '',
            name: '',
            email: '',
            phone: '',
            currentPage: 1,
            perPage: 6,
            authorbooksperPage: 3,
            AuthorbookcurrentPage: 1,
            rows: 0,
            books: [],
            pages: '',
            title: '',
            editauthormodal: false,
            addauthormodal: false,
            Updatedbooksmodal: false,
            authors: [],
            fields: [
                { key: 'id', label: 'ID' },
                { key: 'name', label: 'Name' },
                { key: 'total_books', label: 'Total Books' },
            ],

            bookFields: [
                { key: 'id', label: 'ID' },
                { key: 'name', label: 'Book Title' },
                { key: 'page_numbers', label: 'Page Number' },
            ],

            selectedAuthor: {
                id: '',
                name: '',
                total_books: '',
            },
            Addbooksmodal: false,
            selectedBook: {
                id: '',
                name: '',
                page_numbers: '',
                author_name: '',
            },
        };
    },

    computed: {
        filteredAuthors() {
            // Filter books based on search query
            if (!this.searchQuery) {
                return this.authors;
            }
            const query = this.searchQuery.toLowerCase();
            return this.authors.filter((author) => author.name.toLowerCase().includes(query));
        },
    },

    methods: {
        OpenUpdatedbooksmodal(item, index, event) {
            this.selectedBook = {
                id: item.id,
                name: item.name,
                page_numbers: item.page_numbers,
                author_name: this.selectedAuthor.name,
            };
            console.log(this.selectedBook);
            this.Updatedbooksmodal = true;
        },
        closeAddbookModals() {
            this.Addbooksmodal = false;
        },
        openaddbookmodal() {
            this.Addbooksmodal = true;
        },
        CloseEditModal() {
            this.editauthormodal = false;
        },
        CloseAddModal() {
            this.addauthormodal = false;
        },
        openmodal(item, index, event) {
            this.selectedAuthor = {
                id: item.id,
                name: item.name,
                total_books: item.total_books,
            };

            this.editauthormodal = true;
            this.getauthorbooks();
        },
        addAuthorModal() {
            this.addauthormodal = true;
        },

        async addBookforAuthor() {
            const bookToadd = {
                name: this.title,
                page_numbers: this.pages,
            };

            try {
                const response = await axios.post(
                    `http://127.0.0.1:8000/users/addbook_to_author/${this.selectedAuthor.id}`,
                    bookToadd
                );
                this.books.push(response.data);
                this.title = '';
                this.pages = '';
                this.getauthorbooks();
                this.Addbooksmodal = false;
            } catch (error) {
                console.log(error);
            }
        },

        async getauthorbooks() {
            try {
                const response = await axios.get(
                    `http://127.0.0.1:8000/users/get_author_books/${this.selectedAuthor.id}`
                );
                this.books = response.data.map((book) => {
                    return {
                        id: book.id,
                        name: book.name,
                        page_numbers: book.page_numbers,
                    };
                });
            } catch (error) {
                console.log(error);
            }
        },

        async updateBookById() {
            const updatedBook = {
                name: this.selectedBook.name,
                page_numbers: this.selectedBook.page_numbers,
                author_name: this.selectedAuthor.name,
            };
            try {
                const response = await axios
                    .put(`http://127.0.0.1:8000/users/update_book/${this.selectedBook.id}`, updatedBook)
                    .then(() => {
                        this.getauthorbooks();
                    });

                // console.log(response.data);
                this.Updatedbooksmodal = false;
                this.selectedBook = {
                    id: '',
                    name: '',
                    page_numbers: '',
                    author_name: '',
                };
                this.getauthorbooks();
                this.editauthormodal = false;
            } catch (error) {
                console.log(error);
            }
        },

        onSubmitUpdate(evt) {
            evt.preventDefault();
            this.updateBookById();
            this.getauthorbooks();
        },

        onSubnitForAuthor(evt) {
            evt.preventDefault();
            this.addBookforAuthor();
        },

        async addAuthor() {
            try {
                const response = await axios.post('http://127.0.0.1:8000/users/create_author', {
                    name: this.name,
                });
                this.authors.push(response.data);
                this.name = '';
                this.addauthormodal = false;
            } catch (error) {
                console.log(error);
            }
        },

        onSubmit(evt) {
            evt.preventDefault();
            // call the addAuthor method
            this.addAuthor();
        },

        async deleteAuthorById() {
            try {
                const response = await axios.delete(`http://127.0.0.1:8000/users/delete_book/${this.selectedBook.id}`);
                this.getauthorbooks();
                this.Updatedbooksmodal = false;
            } catch (error) {
                console.log(error);
            }
        },

        async getAuthors() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/users/get_all_authors');
                this.authors = response.data;
            } catch (error) {
                console.log(error);
            }
        },
    },

    mounted() {
        this.getAuthors();
    },
};
</script>

<style></style>
