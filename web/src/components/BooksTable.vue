<template>
    <div>
        <h1>Books</h1>
        <div style="position: fixed; top: 10px; right: 10px; z-index: 1000;">
        <v-alert v-if="errorMessage" v-model="alert" type="error" density="compact" variant="tonal" closable>
            <span v-html="formattedErrorMessage"></span>
        </v-alert>
        <v-alert v-if="successMessage" v-model="alert" type="success" density="compact" variant="tonal" closable>
            <span v-html="formattedSuccessMessage"></span>
        </v-alert>
        </div>
        <div>
            <v-container>
                <v-col cols="12" style="font-size: 14px;">
                    Click the button below to toggle column visibility</v-col>
                <v-row>
                    <v-col cols="12">
                        <v-btn variant="text" :color="visibleColumns.includes('name') ? 'primary' : 'default'"
                            @click="toggleColumnVisibility('name')">
                            Name
                        </v-btn>
                        <v-btn variant="text" :color="visibleColumns.includes('title') ? 'primary' : 'default'"
                            @click="toggleColumnVisibility('title')">
                            Title
                        </v-btn>
                        <v-btn variant="text" :color="visibleColumns.includes('author') ? 'primary' : 'default'"
                            @click="toggleColumnVisibility('author')">
                            Author
                        </v-btn>
                        <v-btn variant="text" :color="visibleColumns.includes('description') ? 'primary' : 'default'"
                            @click="toggleColumnVisibility('description')">
                            Description
                        </v-btn>
                        <v-btn variant="text" :color="visibleColumns.includes('price') ? 'primary' : 'default'"
                            @click="toggleColumnVisibility('price')">
                            Price
                        </v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </div>
        <v-container>
            <v-table>
                <thead>
                    <tr>
                        <th v-if="visibleColumns.includes('name')">Name</th>
                        <th v-if="visibleColumns.includes('title')">Title</th>
                        <th v-if="visibleColumns.includes('author')">Author</th>
                        <th v-if="visibleColumns.includes('description')">Description</th>
                        <th v-if="visibleColumns.includes('price')">Price</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in books" :key="book.id">
                        <td v-if="visibleColumns.includes('name')">{{ book.name }}</td>
                        <td v-if="visibleColumns.includes('title')">{{ book.title }}</td>
                        <td v-if="visibleColumns.includes('author')">{{ book.author }}</td>
                        <td v-if="visibleColumns.includes('description')">{{ book.description }}</td>
                        <td v-if="visibleColumns.includes('price')">{{ book.price }}</td>
                        <td>
                            <v-btn variant="text" color="orange" @click="editBook(book)">Edit</v-btn>
                        </td>
                        <td>
                            <v-btn variant="text" color="red"
                                @click="console.log(book.id); deleteBook(book.id)">Delete</v-btn>
                        </td>
                    </tr>
                </tbody>
            </v-table></v-container>
        <v-container>
            <template v-if="showPrevButton">
                <v-btn variant="text" size="x-small" @click="loadPrev()">Prev page</v-btn>
            </template>
            <template v-if="showNextButton">
                <v-btn variant="text" size="x-small" @click="loadNext()">Next page</v-btn>
            </template></v-container>

        <div v-if="editingBook">
            <v-form @submit.prevent="updateBook">
                <v-container>
                    <v-row>
                        <v-col cols="12" md="2">
                            <v-text-field v-model="editingBook.name" placeholder="Name" required /></v-col>
                        <v-col cols="12" md="2">
                            <v-text-field v-model="editingBook.title" placeholder="Title" /></v-col>
                        <v-col cols="12" md="2">
                            <v-text-field v-model="editingBook.author" placeholder="Author" required /></v-col>
                        <v-col cols="12" md="5">
                            <v-text-field v-model="editingBook.description" placeholder="Description" /></v-col>
                        <v-col cols="12" md="1">
                            <v-text-field v-model="editingBook.price" placeholder="Price" type="number"
                                required /></v-col>
                    </v-row>
                    <v-btn variant="text" color="green" type="submit">Update</v-btn>
                    <v-btn variant="text" color="red" @click="cancelEdit">Cancel</v-btn></v-container>
            </v-form>
        </div>
        <div>
            <v-form @submit.prevent="addBook">
                <v-container>
                    <v-row>
                        <v-col cols="12" md="2">
                            <v-text-field v-model="newBook.name" placeholder="Name" required /></v-col>
                        <v-col cols="12" md="2">
                            <v-text-field v-model="newBook.title" placeholder="Title" /></v-col>
                        <v-col cols="12" md="2">
                            <v-text-field v-model="newBook.author" placeholder="Author" required /></v-col>
                        <v-col cols="12" md="5">
                            <v-text-field v-model="newBook.description" placeholder="Description" /></v-col>
                        <v-col cols="12" md="1">
                            <v-text-field v-model="newBook.price" placeholder="Price" type="number" required /></v-col>
                    </v-row>
                    <v-btn variant="text" color="green" type="submit">Add New Book</v-btn>
                </v-container>
            </v-form>
        </div>
    </div>
</template>

<script>
import apiClient from '@/api';

export default {
    name: 'BooksTable',
    data() {
        return {
            books: [],
            visibleColumns: [],
            profiles: [],
            newBook: {
                name: '',
                title: '',
                author: '',
                description: '',
                price: null
            },
            editingBook: null,
            errorMessage: '',
            successMessage: '',
            currentPage: 1,
            showPrevButton: false,
            showNextButton: false,
            alert: false,
        };
    },
    async mounted() {
        await this.fetchBooks();
        await this.fetchProfiles();
    },
    watch: {
        errorMessage(newVal) {
            if (newVal) {
                this.alert = true;
            }
        },
        successMessage(newVal) {
            if (newVal) {
                this.alert = true;
            }
        },
        alert(newVal) {
            if (newVal) {
                if (this.alertTimeoutId) {
                    clearTimeout(this.alertTimeoutId);
                }
                this.alertTimeoutId = setTimeout(() => {
                    this.alert = false;
                }, 3000);
            } else {
                this.errorMessage = '';
                this.successMessage = '';
                if (this.alertTimeoutId) {
                    clearTimeout(this.alertTimeoutId);
                    this.alertTimeoutId = null;
                }
            }
        },
    },
    methods: {
        async fetchBooks() {
            try {
                const response = await apiClient.get('books/', {
                    params: {
                        page: this.currentPage,
                    },
                });
                this.books = response.data.results;
                this.showNextButton = false
                this.showPrevButton = false
                if (response.data.previous) {
                    this.showPrevButton = true
                }
                if (response.data.next) {
                    this.showNextButton = true
                }
            } catch (error) {
                console.error('Error fetching books:', error);
                this.errorMessage = 'An error occurred while fetching data.';
            }
        },
        loadPrev() {
            this.currentPage -= 1
            this.fetchBooks()
        },
        loadNext() {
            this.currentPage += 1
            this.fetchBooks()
        },
        async fetchProfiles() {
            try {
                const profilesResponse = await apiClient.get('profiles/');
                this.profiles = profilesResponse.data.results;
                this.visibleColumns = this.profiles.filter(profile => profile.is_visible).map(profile => profile.column_name);
            } catch (error) {
                console.error('Error fetching profiles:', error);
            }
        },

        async addBook() {
            try {
                const response = await apiClient.post('books/', this.newBook);
                this.books.push(response.data);
                this.newBook = {
                    name: '',
                    title: '',
                    author: '',
                    description: '',
                    price: null
                };
                this.successMessage = ''
                this.fetchBooks()
                this.successMessage = 'New book was added successfully'
            } catch (error) {
                this.errorMessage = ''
                console.error('Error adding book:', error);
                if (error.response && error.response.data) {
                    for (const field in error.response.data) {
                        if (Array.isArray(error.response.data[field]) && error.response.data[field].length > 0) {
                            this.errorMessage += `${field}: ${error.response.data[field][0]}\n`;
                        }
                    }
                    if (this.errorMessage.endsWith('\n')) {
                        this.errorMessage = this.errorMessage.slice(0, -1);
                    }
                } else {
                    this.errorMessage = 'An unexpected error occurred while adding the book.';
                }
            }
        },

        editBook(book) {
            this.editingBook = { ...book };
        },

        async updateBook() {
            try {
                const response = await apiClient.patch(`books/${this.editingBook.id}/`, this.editingBook);
                const index = this.books.findIndex(book => book.id === response.data.id);
                this.books.splice(index, 1, response.data);
                this.cancelEdit();
                this.successMessage = ''
                this.successMessage = 'The book was updated successfully'
            } catch (error) {
                this.errorMessage = ''
                console.error('Error updating book:', error);
                if (error.response && error.response.data) {
                    for (const field in error.response.data) {
                        if (Array.isArray(error.response.data[field]) && error.response.data[field].length > 0) {
                            this.errorMessage += `${field}: ${error.response.data[field][0]}\n`;
                        }
                    }
                    if (this.errorMessage.endsWith('\n')) {
                        this.errorMessage = this.errorMessage.slice(0, -1);
                    }
                } else {
                    this.errorMessage = 'An unexpected error occurred while updating the book.';
                }
            }
        },

        cancelEdit() {
            this.editingBook = null;
        },

        async deleteBook(bookId) {
            try {
                await apiClient.delete(`books/${bookId}/`);
                await this.fetchBooks();
                this.successMessage = 'Book deleted successfully';
            } catch (error) {
                console.error('Error deleting book:', error, `Book ID: ${bookId}`);
                this.errorMessage = 'An error occurred while deleting the book.';
            }
        },

        async toggleColumnVisibility(column) {
            const index = this.visibleColumns.indexOf(column);
            let updatedProfile;
            if (index > -1) {
                this.visibleColumns.splice(index, 1);
                updatedProfile = { column_name: column, is_visible: false };
            } else {
                this.visibleColumns.push(column);
                updatedProfile = { column_name: column, is_visible: true };
            }
            try {
                await apiClient.patch(`profiles/${column}/`, updatedProfile);
                await this.fetchProfiles();
            } catch (error) {
                console.error('Error updating profile:', error);
            }
        }
    },
    computed: {
        formattedErrorMessage() {
            return this.errorMessage.replace(/\n/g, '<br>');
        },

        formattedSuccessMessage() {
            return this.successMessage.replace(/\n/g, '<br>');
        },
    }
};
</script>
