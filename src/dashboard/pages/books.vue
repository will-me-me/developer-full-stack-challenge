<template>
    <div>
        <b-container style="margin-top: 180px !important">
            <b-row>
                <b-col>
                    <b-card title="" class="mb-2">
                        <template class="">
                            <b-button pill variant="outline-primary" class="mb-2 mr-2" @click="addbooksmodal"
                                >Add Book</b-button
                            >
                            <b-form-input v-model="searchQuery" placeholder="Search" class="mb-2"></b-form-input>
                        </template>
                        <b-card-text>
                            <b-table
                                striped
                                hover
                                :items="filteredBooks"
                                :fields="fields"
                                responsive="sm"
                                class="mt-3 mb-3 text-justify text-muted"
                                :per-page="perPage"
                                :current-page="currentPage"
                                @row-clicked="openmodal"
                            >
                            </b-table>
                            <b-pagination
                                v-model="currentPage"
                                :total-rows="filteredBooks.length"
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
        <!-- modal to add books -->
        <b-modal id="addbook" title="Add Book" size="lg" hide-footer v-model="Addbooksmodal" centered>
            <b-container>
                <b-row>
                    <b-col>
                        <!-- @submit.prevent="onSubmit" @reset="onReset" v-if="show" -->
                        <b-form @submit.prevent="onSubmit">
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
                            <b-form-group id="input-group-2" label="Author:" label-for="input-2">
                                <treeselect
                                    id="input-2"
                                    v-model="author"
                                    :options="getAuthorsNames"
                                    placeholder="Select author"
                                    required
                                    class="mb-3"
                                ></treeselect>

                                <treeselect-value :value="author" />
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

        <!-- modal to edit books -->
        <b-modal id="editbook" title="Edit Book" size="lg" hide-footer v-model="editbookmodal" centered>
            <b-container>
                <b-row>
                    <b-col>
                        <!-- @submit.prevent="onSubmit" @reset="onReset" v-if="show" -->
                        <b-form @submit.prevent="onsubmitEdit">
                            <b-form-group id="input-group-1" label="Title:" label-for="input-1">
                                <b-form-input
                                    id="input-1"
                                    v-model="selectedBook.title"
                                    type="text"
                                    placeholder="Enter title"
                                    required
                                ></b-form-input>
                            </b-form-group>
                            <b-form-group id="input-group-3" label="Price:" label-for="input-3">
                                <b-form-input
                                    id="input-3"
                                    v-model="selectedBook.pages"
                                    type="number"
                                    placeholder="Number of Pages"
                                    required
                                ></b-form-input>
                            </b-form-group>
                            <b-form-group id="input-group-2" label="Author:" label-for="input-2">
                                <treeselect
                                    id="input-2"
                                    v-model="selectedBook.author"
                                    :options="getAuthorsNames"
                                    placeholder="Select author"
                                    required
                                    class="mb-3"
                                ></treeselect>

                                <treeselect-value :value="selectedBook.author" />
                            </b-form-group>
                            <div class="d-flex justify-content-between">
                                <b-button pill type="submit" variant="primary">Submit</b-button>
                                <b-button pill type="reset" variant="danger" @click="deleteBook">Delete</b-button>
                            </div>
                        </b-form>
                    </b-col>
                </b-row>
            </b-container>
        </b-modal>
    </div>
</template>

<script>
// import Treeselect from 'vue-treeselect';
import Treeselect from '@riophae/vue-treeselect';
import '@riophae/vue-treeselect/dist/vue-treeselect.css';
import axios from 'axios';
import { add, get } from 'lodash';
export default {
    middleware: 'auth',

    name: 'books',
    components: {
        Treeselect,
    },
    data() {
        return {
            searchQuery: '',
            currentPage: 1,
            perPage: 5,
            title: '',
            pages: '',
            value: '',
            author: null,
            editbookmodal: false,
            Addbooksmodal: false,
            books: [],
            fields: [
                { key: 'id', label: 'ID' },
                { key: 'name', label: 'Title' },
                { key: 'page_numbers', label: 'Pages' },
                { key: 'author.name', label: 'Author' },
            ],
            authorOptions: [],
            selectedBook: {
                id: '',
                title: '',
                pages: '',
                author: '',
            },
        };
    },
    computed: {
        filteredBooks() {
            // Filter books based on search query
            if (!this.searchQuery) {
                return this.books;
            }
            const query = this.searchQuery.toLowerCase();
            return this.books.filter((book) => book.name.toLowerCase().includes(query));
        },

        getAuthorsNames() {
            return this.authorOptions.map((author) => {
                return {
                    id: author.name,
                    label: author.name,
                };
            });
        },
    },
    created() {},
    methods: {
        async getAuthors() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/users/get_all_authors');
                this.authorOptions = response.data;
            } catch (error) {
                console.log(error);
            }
        },
        openmodal(item, index, event) {
            this.selectedBook = {
                id: item.id,
                title: item.name,
                pages: item.page_numbers,
                author: item.author.name,
            };
            this.editbookmodal = true;
        },
        addbooksmodal() {
            this.Addbooksmodal = true;
        },
        closeAddbookModals() {
            this.Addbooksmodal = false;
        },

        async getBooks() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/users/get_all_books');
                const books = get(response, 'data', []);
                this.books = books;
            } catch (error) {
                console.log(error);
            }
        },

        async addBook() {
            const bookToAdd = {
                name: this.title,
                page_numbers: this.pages,
                author_name: this.author,
            };
            console.log('bookToAdd', bookToAdd);
            try {
                const response = await axios.post('http://127.0.0.1:8000/users/create_book', {
                    ...bookToAdd,
                });
                console.log('response', response);
                this.title = '';
                this.pages = '';
                this.author = null;
                this.Addbooksmodal = false;
                this.getBooks();
            } catch (error) {
                console.log(error);
            }
        },

        async editBook() {
            const bookToEdit = {
                name: this.selectedBook.title,
                page_numbers: this.selectedBook.pages,
                author_name: this.selectedBook.author,
            };

            try {
                const response = await axios.put(`http://127.0.0.1:8000/users/update_book/${this.selectedBook.id}`, {
                    ...bookToEdit,
                });
                this.title = '';
                this.pages = '';
                this.author = null;
                this.editbookmodal = false;
                this.getBooks();
            } catch (error) {
                console.log(error);
            }
        },

        async deleteBook() {
            try {
                const response = await axios.delete(`http://127.0.0.1:8000/users/delete_book/${this.selectedBook.id}`);
                console.log('response', response);
                this.title = '';
                this.pages = '';
                this.author = null;
                this.editbookmodal = false;
                this.getBooks();
            } catch (error) {
                console.log(error);
            }
        },

        onSubmit(evt) {
            evt.preventDefault();
            this.addBook();
        },

        onsubmitEdit(evt) {
            evt.preventDefault();
            this.editBook();
        },
    },
    mounted() {
        this.getBooks();

        this.getAuthors();
    },
};
</script>

<style></style>
