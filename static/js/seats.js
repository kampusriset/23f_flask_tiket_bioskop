function toggleSeat(el){
  if(el.classList.contains('reserved')) return;
  el.classList.toggle('selected');
  updateHidden();
}
function updateHidden(){
  const seats = [...document.querySelectorAll('.seat.selected')].map(s=>s.dataset.seat).join(',');
  const input = document.querySelector('input[name="seats"]');
  if(input) input.value = seats;
  const countEl = document.getElementById('selectedCount');
  if(countEl) countEl.innerText = seats ? seats.split(',').length : 0;
}