document.addEventListener("DOMContentLoaded", () => {
	let form = document.getElementById('form_subir');

	form.addEventListener("submit", function(event) {
		event.preventDefault();
		subir_archivos(this);
	});
});

function subir_archivos(form){
	let barra_estado = form.children[1].children[0],
		span = barra_estado.children[0],
		boton_cancelar = form.children[2].children[1];

		barra_estado.classList.remove('barra_verde', 'barra_roja');


		//peticion
		let peticion = new XMLHttpRequest();

		//progreso
		peticion.upload.addEventListener("progress", (event) => {
			let porcentaje = Math.round((event.loaded / event.total) * 100);

			console.log(porcentaje);

			barra_estado.style.width = porcentaje+'%';
			span.innerHTML = porcentaje+'%';
		});


		//Finalizado
		peticion.addEventListener("load", () => {
			barra_estado.classList.add('barra_verde');
			span.innerHTML = "Proceso Completado";
		});

		//Enviar archivos
		peticion.open('POST', '/uploader');
		peticion.send(new FormData(form));

		

		//cancelar
		boton_cancelar.addEventListener("click", () => {
			peticion.abort();
			barra_estado.classList.remove('barra_verde');
			barra_estado.classList.add('barra_roja');
			span.innerHTML = "Proceso cancelado";
		});

}