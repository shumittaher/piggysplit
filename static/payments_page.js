document.addEventListener("DOMContentLoaded", function() {
    trip_id_area = document.getElementById("trip_id_area")
    trip_desc_area = document.getElementById("trip_desc_area")
    payment_form_area = document.getElementById("payment_form_area")
    participant_options = document.getElementById("participant_options")
    payment_details_table = document.getElementById("payment_details_table")
    payment_details_area = document.getElementById("payment_details_area")
})

function submit_trip(event) {
    const trip_id = event.target.value
    fetch_trip(trip_id)
}

function submit_payment(e) {

    e.preventDefault();
    let formData = new FormData(e.target)
    payment_row = Object.fromEntries(formData); 
    record_payment(payment_row)

}

function place_trips_details(data) {

    let {closed, owner_id, trip_descrip, trip_id, trip_title} = data.trip_data
    let participants = data.participants_data
    let payments = data.payments_data
    
    payment_form_area.hidden = false
    trip_desc_area.innerHTML = `${trip_descrip}`
    trip_id_area.value = `${trip_id}`
    
    participant_options.innerHTML = "<option value='0'>Vendor</option>"
    participants.forEach(participant => {
        participant_options.innerHTML += `
                        <option value="${participant.id}">${participant.username}</option>
                        `
        })
    
    place_payments_details(payments)
}   

function place_payments_details(payments) {

    payment_details_area.innerHTML = ""
    payment_details_table.hidden = true

    if (payments.length > 0) {
        let payee
        payment_details_table.hidden = false
        payments.forEach(payment_row => {
            if (payment_row.username){
                payee = payment_row.username
            } else if (payment_row.paid_to == 0){
                payee = "Vendor"
            }
            payment_details_area.innerHTML += `
                <tr>
                    <td>
                        ${payee}
                    </td>
                    <td>
                        ${payment_row.payment_description}
                    </td>
                    <td class="text-end">
                        ${payment_row.payment_amount}
                    </td>
                    <td>
                        <button onclick="" class="btn-close" aria-label="Remove"></button>
                    </td>
                </tr>
                `
            })
    }
}


function fetch_trip(trip_id) {
    fetch('/trip_payments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "trip_id": trip_id })
    })
    .then(response => response.json())
    .then(data => place_trips_details(data))
    .catch(error => console.error(error));
}


function record_payment(payments_row) {
    fetch('/record_payments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "payments_row": payments_row })
    })
    .then(response => response.json())
    .then(data => place_payments_details(data.payments_data))
    .catch(error => console.error(error));
}