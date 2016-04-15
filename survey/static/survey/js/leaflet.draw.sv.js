L.drawLocal = {
	draw: {
		toolbar: {
			actions: {
				title: 'Avbryt att rita',
				text: 'Avbryt'
			},
			undo: {
				title: 'Ta bort den senast ritade punkten',
				text: 'Ta bort den senaste punkten'
			},
			buttons: {
				polyline: 'Rita en linje',
				polygon: 'Rita en yta',
				rectangle: 'Rita en rektangel',
				circle: 'Rita en cirkel',
				marker: 'Rita en punkt'
			}
		},
		handlers: {
			circle: {
				tooltip: {
					start: 'Klicka och dra för att rita en cirkel.'
				},
				radius: 'Radie'
			},
			marker: {
				tooltip: {
					start: 'Klicka på kartan för att placera punkten.'
				}
			},
			polygon: {
				tooltip: {
					start: 'Klicka för att börja rita formens första sida.',
					cont: 'Klicka för att fortsätta rita formens sidor.',
					end: 'Klicka på den första punkten för att avsluta denna form.'
				}
			},
			polyline: {
				error: '<strong>Funktionsfel:</strong> Linjerna får inte korsa varandra!',
				tooltip: {
					start: 'Klicka för att börja rita en linje.',
					cont: 'Klicka för att fortsätta rita en linje.',
					end: 'Klicka på den sista punkten för att avsluta formen.'
				}
			},
			rectangle: {
				tooltip: {
					start: 'Klicka och dra för att rita en rektangel.'
				}
			},
			simpleshape: {
				tooltip: {
					end: 'Släpp musen för att avsluta din ritning.'
				}
			}
		}
	},
	edit: {
		toolbar: {
			actions: {
				save: {
					title: 'Spara ändringar.',
					text: 'Spara'
				},
				cancel: {
					title: 'Avbryt redigering, spara inga ändringar.',
					text: 'Avbryt.'
				}
			},
			buttons: {
				edit: 'Redigera lager.',
				editDisabled: 'Inga lager att redigera.',
				remove: 'Radera lager.',
				removeDisabled: 'Inga lager att radera.'
			}
		},
		handlers: {
			edit: {
				tooltip: {
					text: 'Dra ettverktyg, eller klicka med markören, för att redigera ett innehåll.',
					subtext: 'Klicka avbryt för att ta bort ändringar.'
				}
			},
			remove: {
				tooltip: {
					text: 'Klicka på ett innehåll för att radera det.'
				}
			}
		}
	}
};
