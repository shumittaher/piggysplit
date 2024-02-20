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
    jason_fetch("trip_payments", trip_id, place_trips_details)
}

function submit_payment(e) {
    e.preventDefault();
    let formData = new FormData(e.target)
    payment_row = Object.fromEntries(formData); 

    jason_fetch("record_payments", payment_row, place_payments_details)

}


function handle_delete(payment_id, trip_id) {
    jason_fetch("delete_payments", {payment_id, trip_id},place_payments_details)        
}

function jason_fetch(route_name, data, result_function) {
    fetch(`/${route_name}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "data" : data })
    })
    .then(response => response.json())
    .then(result => result_function(result))
    .catch(error => console.error(error));
}

function place_trips_details(data) {

    let {closed, owner_id, trip_descrip, trip_id, trip_title} = data.trip_data
    let participants = data.participants_data
    
    payment_form_area.hidden = false
    trip_desc_area.innerHTML = `${trip_descrip}`
    trip_id_area.value = `${trip_id}`
    
    participant_options.innerHTML = "<option value='0'>Vendor</option>"
    participants.forEach(participant => {
        participant_options.innerHTML += `
                        <option value="${participant.id}">${participant.username}</option>
                        `
        })
    
    place_payments_details(data)
}   

function place_payments_details(data) {

    let payments = data.payments_data

    payment_details_area.innerHTML = ""
    payment_details_table.hidden = true

    if (payments.length > 0) {
        let payee
        payment_details_table.hidden = false
        payments.forEach(payment_row => {
            if (payment_row.payeename){
                payee = payment_row.payeename
            } else {
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
                    <td class="text-end">
                        ${payment_row.payer_name}
                    </td>
                    <td>
                        <button onclick="handle_delete(${payment_row.payment_id}, ${payment_row.trip_id})" class="btn-close" aria-label="Remove"></button>
                    </td>
                </tr>
                `
            })
    }
}