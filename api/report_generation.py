from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io

class ReportGenerator:
    @staticmethod
    def create_pdf_report(energy_data, daily_imbalance, highest_imbalance_hour):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=10*mm, leftMargin=10*mm, topMargin=10*mm, bottomMargin=10*mm)
        elements = []

        styles = getSampleStyleSheet()
        
        # Title
        elements.append(Paragraph("Energy Data Report", styles['Title']))
        elements.append(Spacer(1, 6*mm))

        # Daily Imbalance
        elements.append(Paragraph("Daily Imbalance", styles['Heading2']))
        data = [
            ['Date', 'Total Cost', 'Unit Rate'],
            [daily_imbalance['date'], f"£{daily_imbalance['total_daily_imbalance_cost']:.2f}", f"£{daily_imbalance['daily_imbalance_unit_rate']:.2f}/MWh"]
        ]
        t = Table(data, colWidths=[60*mm, 60*mm, 60*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 6*mm))

        # Highest Imbalance Hour
        elements.append(Paragraph("Highest Imbalance Hour", styles['Heading2']))
        data = [
            ['Date', 'Hour', 'Volume'],
            [highest_imbalance_hour['date'], f"{highest_imbalance_hour['highest_imbalance_hour']}:00", f"{highest_imbalance_hour['highest_imbalance_volume']:.2f} MWh"]
        ]
        t = Table(data, colWidths=[60*mm, 60*mm, 60*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 6*mm))

        # Graph
        plt.figure(figsize=(8, 4))
        settlement_periods = [point.settlement_period for point in energy_data.data_points]
        net_imbalance_volumes = [point.net_imbalance_volume for point in energy_data.data_points]
        
        plt.plot(settlement_periods, net_imbalance_volumes)
        plt.title('Net Imbalance Volume Over Settlement Periods')
        plt.xlabel('Settlement Period')
        plt.ylabel('Net Imbalance Volume (MWh)')
        plt.xticks(range(0, 49, 4))  # Show every 4th settlement period
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300)
        img_buffer.seek(0)
        img = Image(img_buffer)
        img.drawHeight = 100*mm
        img.drawWidth = 180*mm
        elements.append(img)

        elements.append(PageBreak())

        # Detailed table
        elements.append(Paragraph("Detailed Energy Data", styles['Heading2']))
        data = [['Period', 'Start Time', 'System Sell Price (£)', 'System Buy Price (£)', 'Net Imbalance Volume (MWh)']]
        for point in energy_data.data_points:
            data.append([
                point.settlement_period,
                point.start_time,
                f"{point.system_sell_price:.2f}",
                f"{point.system_buy_price:.2f}",
                f"{point.net_imbalance_volume:.2f}"
            ])
        
        t = Table(data, colWidths=[20*mm, 40*mm, 40*mm, 40*mm, 40*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)

        # Build the PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer