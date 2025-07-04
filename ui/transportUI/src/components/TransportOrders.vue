<template>
    <div>
        <div class="header-bar">
            <h1 class="header-title">Simple Transport Management System</h1>
        </div>

        <div class="page-wrapper">

            <div class="tabs">
                <button :class="{ active: activeTab === 'table' }" @click="activeTab = 'table'">Orders</button>
                <button :class="{ active: activeTab === 'add'}" @click="startAdd">Create</button>
            </div>

            <div v-if="activeTab === 'table'" class="table-container">
                <h2 class="table-title">Transport Orders</h2>

                <div class="filters" style="margin-bottom: 1rem; display: flex; gap: 1rem; align-items: center; color: #ddd;">
                    <label>
                        From:
                        <input type="date" v-model="filterStartDate" class="uniform-input"/>
                    </label>
                    <label>
                        To:
                        <input type="date" v-model="filterEndDate" class="uniform-input"/>
                    </label>
                    <label>
                        Customer Name:
                        <input type="text" v-model="filterCustomerName" class="uniform-input"/>
                    </label>
                    <button @click="applyFilters" class="find-reset-button">Find</button>
                    <button @click="resetFilters" class="find-reset-button">Reset Filter</button>
                </div>

                <table class="orders-table" cellpadding="5" cellspacing="0" border="0">
                    <thead>
                        <tr>
                            <th>Order Number</th>
                            <th>Customer Name</th>
                            <th>Date</th>
                            <th>Waypoints</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="filteredOrders.length === 0">
                            <td colspan="5" style="text-align: center; color: #aaa;">No data</td>
                        </tr>
                        <tr v-else v-for="order in filteredOrders" :key="order.id">
                            <td>{{ order.order_number }}</td>
                            <td>{{ order.customer_name }}</td>
                            <td>{{ order.date }}</td>
                            <td>
                                <ul>
                                <li v-for="(wp, idx) in order.waypoints" :key="idx">
                                {{ wp.location_name }} ({{ wp.waypoint_type }})
                                </li>
                                </ul>
                            </td>
                            <td>
                                <button class="edit-btn" @click="startEdit(order)">Edit</button>
                                <button class="delete-btn" @click="deleteOrder(order.id)">Delete</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="activeTab === 'add' || activeTab === 'edit'" class="form-container">
                <h2>{{ activeTab === 'add' ? 'Create New Order' : 'Edit order' }}</h2>
                <form @submit.prevent="activeTab === 'add' ? submitOrder() : updateOrder()">
                    <label>
                        Order Number:
                        <input v-model="newOrder.order_number" type="text" required />
                    </label>
                    <label>
                        Customer Name:
                        <input v-model="newOrder.customer_name" type="text" required />
                    </label>
                    <label>
                        Date:
                        <input v-model="newOrder.date" type="date" required />
                    </label>

                    <div class="waypoint-inputs">
                        Waypoint:
                        <input
                            v-model="currentWaypoint.location_name"
                            type="text"
                            placeholder="Location (e.g. Kosice)"
                        />
                        <select v-model="currentWaypoint.waypoint_type">
                            <option disabled value="">Waypoint Type</option>
                            <option value="Pickup">Pickup</option>
                            <option value="Delivery">Delivery</option>
                        </select>
                        <button type="button" @click="addWaypoint" :disabled="!canAddWaypoint">Add waypoint</button>
                    </div>

                    <div v-if="newOrder.waypoints.length" class="waypoints-list">
                        <ul>
                            <li v-for="(wp, idx) in newOrder.waypoints" :key="idx">
                                {{ wp.location_name }} ({{ wp.waypoint_type }})
                                <button type="button" @click="removeWaypoint(idx)" class="remove-wp-btn">×</button>
                            </li>
                        </ul>
                    </div>

                    <button type="submit">{{ activeTab === 'add' ? 'Create Order' : 'Save Changes' }}</button>
                    <button type="button" v-if="activeTab === 'edit'" @click="cancelEdit" style="margin-left:10px;">Cancel</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const filterStartDate = ref<string>('')
const filterEndDate = ref<string>('')
const filterCustomerName = ref<string>('')

const filtersApplied = ref({
    start: '',
    end: '',
    name: ''
})

const filteredOrders = computed(() => {
    return orders.value.filter(order => {
        const orderDate = new Date(order.date)
        const start = filtersApplied.value.start ? new Date(filtersApplied.value.start) : null
        const end = filtersApplied.value.end ? new Date(filtersApplied.value.end) : null
        const nameFilter = filtersApplied.value.name

        if (start && orderDate < start) return false
        if (end && orderDate > end) return false
        if (nameFilter && order.customer_name.toLowerCase() !== nameFilter) return false

        return true
    })
})

function applyFilters() {
    filtersApplied.value.start = filterStartDate.value
    filtersApplied.value.end = filterEndDate.value
    filtersApplied.value.name = filterCustomerName.value.trim().toLowerCase()
}

function resetFilters() {
    filterStartDate.value = '';
    filterEndDate.value = '';
    filterCustomerName.value = '';
    filtersApplied.value.start = '';
    filtersApplied.value.end = '';
    filtersApplied.value.name = '';
}

interface Waypoint {
    location_name: string
    waypoint_type: string
}

interface TransportOrder {
    id: number
    order_number: string
    customer_name: string
    date: string
    waypoints: Waypoint[]
}

const orders = ref<TransportOrder[]>([])

const fetchOrders = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/transportorder/')
        orders.value = response.data
    } catch (error) {
        console.error('Failed to fetch orders:', error)
    }
}

onMounted(() => {
    fetchOrders()
})

const activeTab = ref<'table' | 'add' | 'edit'>('table')

const newOrder = ref<Omit<TransportOrder, 'id'>>({
    order_number: '',
    customer_name: '',
    date: '',
    waypoints: [],
})

const currentWaypoint = ref<Waypoint>({
    location_name: '',
    waypoint_type: '',
})

const canAddWaypoint = computed(() =>
    currentWaypoint.value.location_name.trim() !== '' &&
    currentWaypoint.value.waypoint_type.trim() !== ''
)

function addWaypoint() {
    if (!canAddWaypoint.value) return
        newOrder.value.waypoints.push({
        location_name: currentWaypoint.value.location_name.trim(),
        waypoint_type: currentWaypoint.value.waypoint_type.trim(),
    })
    currentWaypoint.value.location_name = ''
    currentWaypoint.value.waypoint_type = ''
}

function removeWaypoint(index: number) {
    newOrder.value.waypoints.splice(index, 1)
}

const editingOrderId = ref<number | null>(null)

function startAdd() {
    activeTab.value = 'add'
    resetForm()
}

function startEdit(order: TransportOrder) {
    activeTab.value = 'edit'
    editingOrderId.value = order.id

    newOrder.value = {
        order_number: order.order_number,
        customer_name: order.customer_name,
        date: order.date,
        waypoints: JSON.parse(JSON.stringify(order.waypoints)),
    }
    currentWaypoint.value = {
        location_name: '',
        waypoint_type: '',
    }
}

function cancelEdit() {
    activeTab.value = 'table'
    editingOrderId.value = null
    resetForm()
}

function resetForm() {
    newOrder.value = {
        order_number: '',
        customer_name: '',
        date: '',
        waypoints: [],
    }
    currentWaypoint.value = {
        location_name: '',
        waypoint_type: '',
    }
}

const submitOrder = async () => {
    if (newOrder.value.waypoints.length === 0) {
        alert('Please add at least one waypoint.')
        return
    }

    try {
        const response = await axios.post('http://127.0.0.1:8000/api/transportorder/', newOrder.value)
        orders.value.push(response.data)
        resetForm()
        activeTab.value = 'table'
    } catch (error) {
        console.error('Failed to add order:', error)
    }
}

const updateOrder = async () => {
    if (editingOrderId.value === null) {
        alert('Non-existent order ID for modification.')
        return
    }

    if (newOrder.value.waypoints.length === 0) {
        alert('Please add at least one waypoint.')
        return
    }

    try {
        const response = await axios.put(
            `http://127.0.0.1:8000/api/transportorder/${editingOrderId.value}/`,
            newOrder.value
        )
        const index = orders.value.findIndex(o => o.id === editingOrderId.value)
        if (index !== -1) {
            orders.value[index] = response.data
        }
        resetForm()
        editingOrderId.value = null
        activeTab.value = 'table'
    } catch (error) {
        console.error('Failed to update order:', error)
    }
}

const deleteOrder = async (orderId: number) => {
    if (!confirm('Do you really want to delete this order?')) return

    try {
        await axios.delete(`http://127.0.0.1:8000/api/transportorder/${orderId}/`)
        orders.value = orders.value.filter(order => order.id !== orderId)
    } catch (error) {
        console.error('Error deleting order::', error)
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

body {
    background-color: #ffffff;
    margin: 0;
    font-family: 'Inter', sans-serif;
    color: #222222;
}

.header-bar {
    width: 100vw;
    margin: 0;
    padding: 1rem 2rem;
    background-color: #18182f;
    color: white;
    font-weight: bold;
    font-size: 1.5rem;
    text-align: left;
    box-sizing: border-box;
    flex-shrink: 0;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
}

.header-title {
    color: #ffffff;
    font-weight: 700;
    font-size: 1.8rem;
    margin: 0;
    user-select: none;
}

.page-wrapper {
    max-width: 1000px;
    margin: 2rem auto 4rem auto;
    padding: 0 20px;
    font-family: 'Inter', sans-serif;
    color: #222222;
    border-radius: 12px;
}

.table-container {
    background-color: #18182f;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5), 0 2px 6px rgba(0, 0, 0, 0.3);
    overflow-x: auto;
    padding: 20px;
    max-height: 500px;
    overflow-y: auto;
}

.table-title {
    color: #ddd;
    margin-bottom: 12px;
    font-weight: 600;
    font-size: 1.4rem;
    user-select: none;
}

.orders-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 12px;
    font-size: 1rem;
    border-radius: 12px;
    min-width: 700px;
}

.orders-table thead tr {
    background-color: #303050;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
}

.orders-table th,
.orders-table td {
    padding: 12px 18px;
    text-align: center;
    vertical-align: middle;
    font-weight: 500;
    color: #ddd;
    border: none;
    background: transparent;
}

.orders-table tbody tr {
    background-color: #303050;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
    transition: background-color 0.3s ease;
    cursor: default;
    overflow: hidden;
}

.orders-table tbody tr:hover {
    background-color: #444466;
    cursor: default;
}

.orders-table tbody tr td ul {
    list-style-type: none;
    padding-left: 0;
    margin: 0;
    font-weight: 400;
    font-size: 0.9rem;
    color: #bbb;
}

.orders-table tbody tr td ul li {
    margin: 4px 0;
}

.form-container {
    margin-top: 2rem;
    background-color: #18182f;
    padding: 20px;
    border-radius: 12px;
    color: #eee;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5), 0 2px 6px rgba(0, 0, 0, 0.3);
}

.form-container h2 {
    margin-top: 0;
    margin-bottom: 1rem;
    font-weight: 600;
}

.form-container label {
    display: block;
    margin-bottom: 1rem;
    font-weight: 600;
}

.form-container input,
.form-container select {
    width: 100%;
    padding: 8px;
    border-radius: 6px;
    border: none;
    font-size: 1rem;
    box-sizing: border-box;
    margin-top: 4px;
}

.form-container button {
    background-color: #303050;
    color: #ddd;
    padding: 10px 18px;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 1rem;
}

.form-container button:hover:not(:disabled) {
    background-color: #444466;
}

.form-container button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.tabs button {
    background-color: #303050;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    color: #ddd;
    cursor: pointer;
    font-weight: 600;
    transition: background-color 0.3s ease;
}

.tabs button.active,
.tabs button:hover {
    background-color: #444466;
    color: white;
}

.waypoint-inputs {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 1rem;
    align-items: center;
}

.waypoint-inputs input,
.waypoint-inputs select {
    flex: 1;
    min-width: 150px;
}

.waypoints-list ul {
    list-style-type: none;
    padding-left: 0;
    margin: 0;
    color: #ccc;
}

.waypoints-list li {
    margin: 5px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.remove-wp-btn {
    background: transparent;
    border: none;
    color: #ff5555;
    font-weight: 900;
    font-size: 0.9rem;
    cursor: pointer;
    user-select: none;
    padding: 0 9px;
    line-height: 1;
    transition: color 0.2s ease;
    height: 1.5em;
    display: flex;
    align-items: center;
    justify-content: center;
}

.delete-btn {
    background-color: #d91b5c;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: background-color 0.3s ease;
}

.delete-btn:hover {
    background-color: #d91b5c;
}

.waypoints-edit ul {
    list-style-type: none;
    padding-left: 0;
    margin: 0 0 0.5rem 0;
    color: #ccc;
}

.waypoints-edit li {
    margin: 4px 0;
    display: flex;
    gap: 6px;
    align-items: center;
}

.waypoints-edit input {
    padding: 4px 6px;
    border-radius: 6px;
    border: none;
    font-size: 0.9rem;
    flex: 1;
}

.waypoints-edit select {
    padding: 4px 6px;
    border-radius: 6px;
    border: none;
    font-size: 0.9rem;
}

.remove-wp-btn {
    background-color: #900;
    border: none;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    line-height: 18px;
    padding: 0;
    user-select: none;
}

.edit-btn {
    background-color: transparent;
    border: none;
    cursor: pointer;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.9rem;
    transition: color 0.3s ease;
    color: #99aaff;
    user-select: none;
    margin-right: 5px;
}

.edit-btn:hover {
    color: #66ccff;
}

.uniform-input {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14px;
    padding: 8px 12px;
    border: 1.5px solid #444;
    border-radius: 5px;
    outline: none;
    box-sizing: border-box;
    width: 100%;
    transition: border-color 0.3s ease;
}

.uniform-input:focus {
    border-color: #007bff;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.find-reset-button {
    background-color: #303050;
    color: #ddd;
    padding: 10px 18px;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 1.5rem;
}

.find-reset-button:hover:not(:disabled) {
    background-color: #444466;
}

.find-reset-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style>